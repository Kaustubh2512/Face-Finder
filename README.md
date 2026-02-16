# Face Finder

Face Finder is a Python-based tool for identifying and matching faces in event photos against a set of known faces. It uses the `insightface` library for high-accuracy face recognition.

## Features
- Scans a directory of event photos and compares faces to a directory of known individuals.
- Organizes matched photos into folders per person.
- Generates CSV and JSON reports of all matches.
- Annotates photos with detected names and confidence scores.

## Project Structure
- `face_finder1.py`: Main CLI script for face matching.
- `LICENSE`: MIT License.
- `CONTRIBUTING.md`: Guidelines for contributing.
- `requirements.txt`: Project dependencies.

## Requirements
- Python 3.7+
- A compatible C++ compiler (for `insightface` dependencies)
- Required Python packages:
  - `insightface`
  - `onnxruntime` (or `onnxruntime-gpu`)
  - `opencv-python`
  - `numpy`
  - `pandas`
  - `tqdm`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Kaustubh2512/Face-Finder.git
   cd Face-Finder
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 Web UI (Recommended)
Run the premium interactive dashboard:
```bash
streamlit run app.py
```

### 💻 Command Line
Run the script directly via CLI:
```bash
python face_finder1.py --known "Known" --photos "Event Photos" --output "output"
```
*Note: Use `python face_finder1.py --help` to see all available options.*

3. Results will be saved in the `output/` folder:
   - `annotated/`: Images with bounding boxes and names.
   - `per_person/`: Original images sorted into folders by person name.
   - `reports/`: CSV and JSON files detailing all matches.

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
- [Kaustubh Andure](https://github.com/Kaustubh2512)

## Acknowledgements
- Powered by the [InsightFace](https://github.com/deepinsight/insightface) project.
