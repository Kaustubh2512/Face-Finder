from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd

try:
    from insightface.app import FaceAnalysis
except Exception as e:
    raise SystemExit(
        "Failed to import insightface. Install with: pip install insightface onnxruntime"
    ) from e

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image(p: Path) -> bool:
    return p.suffix.lower() in IMG_EXTS


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(np.float32)
    b = b.astype(np.float32)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def read_image_bgr(path: Path) -> np.ndarray:
    img = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image: {path}")
    return img


def save_image_bgr(path: Path, img: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower() or ".jpg"
    success, buf = cv2.imencode(ext, img)
    if not success:
        raise ValueError(f"Could not encode image: {path}")
    path.write_bytes(buf.tobytes())


def collect_files(root: Path):
    return [p for p in root.rglob("*") if p.is_file() and is_image(p)]


def load_face_app(det_size: int = 640):
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(det_size, det_size))
    return app


def build_known_embeddings(app: FaceAnalysis, known_dir: Path, min_size: int):
    people = {}
    for person_dir in sorted(p for p in known_dir.iterdir() if p.is_dir()):
        embs = []
        for img_path in collect_files(person_dir):
            try:
                img = read_image_bgr(img_path)
                faces = app.get(img)
                if not faces:
                    continue
                f0 = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
                x1, y1, x2, y2 = map(int, f0.bbox)
                if (x2 - x1) < min_size or (y2 - y1) < min_size:
                    continue
                emb = f0.embedding
                if emb is not None:
                    embs.append(emb.astype(np.float32))
            except:
                continue
        if embs:
            mean_emb = np.mean(np.stack(embs, axis=0), axis=0)
            norm = np.linalg.norm(mean_emb)
            if norm > 0:
                mean_emb = mean_emb / norm
            people[person_dir.name] = mean_emb.astype(np.float32)
    return people


def annotate_image(img, faces_info):
    out = img.copy()
    for (x1, y1, x2, y2), name, score in faces_info:
        cv2.rectangle(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{name} {score:.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        y_rect = max(0, y1 - th - 8)
        cv2.rectangle(out, (x1, y_rect), (x1 + tw + 8, y_rect + th + 8), (0, 255, 0), -1)
        cv2.putText(out, label, (x1 + 4, y_rect + th + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    return out


def process_event_photos(app, people_embs, photos_dir, out_dir, sim_threshold, min_face):
    annotated_dir = out_dir / "annotated"
    per_person_dir = out_dir / "per_person"
    reports_dir = out_dir / "reports"
    annotated_dir.mkdir(parents=True, exist_ok=True)
    per_person_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    summary = {name: [] for name in people_embs.keys()}

    files = collect_files(photos_dir)
    for img_path in tqdm(files, desc="Scanning photos"):
        try:
            img = read_image_bgr(img_path)
        except:
            continue
        faces = app.get(img)
        face_infos = []
        matches_in_photo = []
        for f in faces:
            x1, y1, x2, y2 = map(int, f.bbox)
            if (x2 - x1) < min_face or (y2 - y1) < min_face:
                continue
            emb = f.embedding
            if emb is None:
                continue
            emb = emb.astype(np.float32)
            n = np.linalg.norm(emb)
            if n > 0:
                emb = emb / n

            best_name = None
            best_score = -1.0
            for name, ref_emb in people_embs.items():
                score = cosine_similarity(emb, ref_emb)
                if score > best_score:
                    best_score = score
                    best_name = name

            if best_name and best_score >= sim_threshold:
                face_infos.append(((x1, y1, x2, y2), best_name, best_score))
                matches_in_photo.append((best_name, best_score))

        if matches_in_photo:
            ann = annotate_image(img, face_infos)
            ann_path = annotated_dir / (img_path.stem + "_annotated" + img_path.suffix)
            save_image_bgr(ann_path, ann)

            for name, _ in matches_in_photo:
                dst = per_person_dir / name / img_path.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                try:
                    dst.write_bytes(Path(img_path).read_bytes())
                except:
                    pass

            rows.append({
                "photo": str(img_path),
                "annotated": str(ann_path.resolve()),
                "matches": ",".join(sorted({m[0] for m in matches_in_photo})),
                "scores": json.dumps({name: float(score) for name, score in matches_in_photo}),
            })
            for name, score in matches_in_photo:
                summary[name].append({"photo": str(img_path), "score": float(score)})

    df = pd.DataFrame(rows)
    csv_path = reports_dir / "matches.csv"
    json_path = reports_dir / "matches.json"
    df.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps({"matches": summary}, indent=2))
    return df


def main():
    base_path = Path(r"C:\Projects\FACE FINDER")
    known_dir = base_path / "Known"
    photos_dir = base_path / "Event Photos"
    out_dir = base_path / "output"

    sim_threshold = 0.35
    det_size = 640
    min_face = 60

    print("Loading face models...")
    app = load_face_app(det_size=det_size)

    print("Building reference embeddings...")
    people_embs = build_known_embeddings(app, known_dir, min_size=min_face)
    if not people_embs:
        raise SystemExit("No valid reference faces found!")

    print(f"Loaded: {', '.join(people_embs.keys())}")
    df = process_event_photos(app, people_embs, photos_dir, out_dir, sim_threshold, min_face)

    print("\nDone!")
    print(f"CSV: {out_dir / 'reports' / 'matches.csv'}")
    print(f"JSON: {out_dir / 'reports' / 'matches.json'}")


if __name__ == "__main__":
    main()
