import numpy as np
from pathlib import Path
from face_finder1 import cosine_similarity, is_image

def test_cosine_similarity_identical():
    # Test that identical vectors have similarity of 1.0
    v1 = np.array([1, 0, 0], dtype=np.float32)
    v2 = np.array([1, 0, 0], dtype=np.float32)
    assert abs(cosine_similarity(v1, v2) - 1.0) < 1e-6

def test_cosine_similarity_orthogonal():
    # Test that orthogonal vectors have similarity of 0.0
    v1 = np.array([1, 0, 0], dtype=np.float32)
    v2 = np.array([0, 1, 0], dtype=np.float32)
    assert abs(cosine_similarity(v1, v2) - 0.0) < 1e-6

def test_cosine_similarity_opposite():
    # Test that opposite vectors have similarity of -1.0
    v1 = np.array([1, 0, 0], dtype=np.float32)
    v2 = np.array([-1, 0, 0], dtype=np.float32)
    assert abs(cosine_similarity(v1, v2) - (-1.0)) < 1e-6

def test_is_image_valid():
    assert is_image(Path("test.jpg")) is True
    assert is_image(Path("photo.PNG")) is True
    assert is_image(Path("image.webp")) is True

def test_is_image_invalid():
    assert is_image(Path("document.pdf")) is False
    assert is_image(Path("script.py")) is False
    assert is_image(Path("README")) is False
