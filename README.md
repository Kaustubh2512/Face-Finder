# 👤 Face Finder

Face Finder is a high-performance, AI-powered tool for identifying and matching faces in large collections of event photos against a set of known individuals. It is designed to automate the process of sorting photos for groups, trek teams, or event attendees.

## 🚀 Key Features
- **High-Speed Processing**: Optimized with `onnxruntime-gpu` for 10x faster scanning.
- **Fast Mode**: Option to run at lower resolutions for 2-3x additional speedup.
- **Automatic Sorting**: Automatically creates folders for each identified person.
- **Flexible Inputs**: Supports both structured folders and direct images as references.
- **Cloud Ready**: Run directly in Google Colab to avoid using local storage.
- **Interactive UI**: Built-in Streamlit dashboard for local use.

---

## ☁️ Running in Google Colab (Recommended)
The fastest way to use Face Finder without installing anything on your computer.

1.  **Open the Notebook**: Upload `Face_Finder_Colab.ipynb` to [Google Colab](https://colab.research.google.com/).
2.  **Enable GPU**: Go to `Runtime > Change runtime type` and select **T4 GPU**.
3.  **Mount Drive**: Run the first cell to connect your Google Drive.
4.  **Configure & Run**: Update your folder paths and hit "Run All".

### 📂 How to Share with a Group:
Once the processing is finished:
1.  Open your Google Drive and find the `Output/per_person/` folder.
2.  **Right-click > Share** this folder with your group via a "Anyone with link" access.
3.  Each person can enter the folder named after them and download only their own photos!

---

## 💻 Local Installation

### Prerequisites
- Python 3.8+
- (Optional) NVIDIA GPU with CUDA for acceleration.

### Setup
```bash
git clone https://github.com/0xYuvi/Face-Finder.git
cd Face-Finder
pip install -r requirements.txt
```

### Usage (Web UI)
```bash
streamlit run app.py
```

### Usage (CLI)
```bash
python face_finder1.py --known "./Known" --photos "./Events" --output "./Results" --use-gpu
```

---

## 🛠️ Configuration
- `--known`: Directory containing reference faces (folders or direct images).
- `--photos`: Directory containing event photos to scan.
- `--output`: Directory to save annotated images and sorted folders.
- `--threshold`: Similarity threshold (default: 0.35). Lower for more matches, higher for accuracy.
- `--det-size`: Detection resolution (320 for speed, 640 for accuracy).
- `--use-gpu`: Enable GPU acceleration.

## ⚖️ License
Distributed under the **MIT License**. See `LICENSE` for more information.

## 🤝 Contributing
Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines.
