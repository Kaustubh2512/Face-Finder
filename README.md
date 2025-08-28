# Face Finder

Face Finder is a Python-based tool for identifying and matching faces in event photos against a set of known faces. It is designed to automate the process of finding individuals in large collections of images, such as those taken at events.

## Features
- Scans a directory of event photos and compares faces to a directory of known individuals
- Outputs results to a specified folder
- Easy to use and configure

## Folder Structure
- `face_finder1.py`: Main Python script for face matching
- `Event Photos/`: Directory containing event images to be scanned
- `Known/`: Directory containing images of known individuals
- `output/`: Directory where results and matched images are saved

## Requirements
- Python 3.7+
- Required Python packages (install with pip):
  - face_recognition
  - opencv-python
  - numpy

## Installation
1. git clone https://github.com/Kaustubh2512/Face-Finder (Clone this repository).
2. Install the required packages:
   cd Face Finder
   pip install -r requirements.txt


## Usage
1. Place images of known individuals in the `Known/` folder.
2. Place event photos in the `Event Photos/` folder.
3. Run the script:
   ```powershell
   python face_finder1.py
   ```
4. Results will be saved in the `output/` folder.

## Customization
- You can modify the script to change input/output directories or adjust matching thresholds as needed.

## License
This project is provided under the MIT License.

## Author
- Kaustubh Andure

## Acknowledgements
- Uses the [face_recognition](https://github.com/ageitgey/face_recognition) library for face detection and recognition.
