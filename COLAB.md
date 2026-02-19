# ☁️ Using Face Finder on Google Colab

This guide explains how to use Face Finder in the cloud to process event photos stored on Google Drive.

## 🚀 Setup Steps

### 1. Upload the Notebook
- Download `Face_Finder_Colab.ipynb` from this repository.
- Go to [Google Colab](https://colab.research.google.com/).
- Click **File > Upload notebook** and select the file.

### 2. Enable GPU (Critical for Speed)
To process 100s of photos in minutes:
- Go to **Runtime > Change runtime type**.
- Select **T4 GPU** (or any available GPU).
- Click **Save**.

### 3. Prepare your Folders
Ensure your Google Drive has the following structure:
- `Known/`: A folder containing high-quality photos of the people you want to find. (Can be subfolders per person or just named images).
- `Event_Photos/`: The folder containing all the photos from your event.

#### 💡 How to use a Shared Folder (Shared Link):
If the photos are in a shared link from someone else, you must add them to your own Drive for Colab to see them:
1.  **Open the Link**: Open the Google Drive shared link in your browser.
2.  **Add Shortcut**: 
    - Click the folder name at the top.
    - Select **Organize** > **Add shortcut**.
    - Choose **My Drive** as the destination.
3.  **Confirm**: Go to your [Google Drive](https://drive.google.com/) and verify the folder appears with a small "arrow" icon.
4.  **Colab Path**: In the notebook, your path will now be `/content/drive/MyDrive/YOUR_SHORTCUT_NAME`.

## 🏃‍♂️ Running the Tool

1.  **Mount Drive**: Run the first cell and authorize Google Drive access.
2.  **Install Libraries**: Run the setup cell. This will install the AI models and GPU drivers.
3.  **Set Paths**: Update the `KNOWN_FACES` and `EVENT_PHOTOS` variables in the config cell to match your Drive paths.
4.  **Process**: Run the final cell.

## 👥 Sharing Results with a Group
Face Finder automatically sorts photos into individual folders.

1.  Navigate to your `Output/per_person/` folder in Google Drive.
2.  Select the folder, click **Share**, and set it to **"Anyone with the link can view"**.
3.  Send the link to your group (e.g., on WhatsApp/Slack).
4.  **Bonus**: Group members can simply open their named folder and download their personal set of photos without seeing everyone else's.

## ⚙️ Troubleshooting
- **No faces found**: Ensure your "Known" photos are clear and front-facing.
- **Too slow**: Verify that "Applied providers" in the logs shows `CUDAExecutionProvider`. If not, check "Enable GPU" instruction above.
- **Path not found**: Remember that Linux is case-sensitive (`data` is different from `Data`).
