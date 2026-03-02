# Sign Language Converter

This project converts Sign Language (ASL) to Text using your webcam and Text to Sign Language images.

## Quick Start (Easiest Way)

1.  **Double-click `run.bat`**: This script will automatically install dependencies, create placeholder images, and start the application for you.

## Manual Setup Instructions

1.  **Install Python**: Download and install Python 3.x from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation.
2.  **Install VS Code** (Optional): A good code editor.
3.  **Install Dependencies**:
    Open a terminal/command prompt in this folder and run:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Run the Main Application**:
    ```bash
    python main.py
    ```
    This will open a GUI with buttons for each step.

## Usage Steps

### 1. Collect Data (Sign to Text)
   - Click "Collect Data".
   - The camera will open.
   - It will ask you to collect data for class 0, 1, 2... (You can map these to A, B, C...).
   - Press 'Q' when you are ready to start recording for a class.
   - Move your hand in front of the camera to capture different angles.
   - It will collect 100 samples per class.

### 2. Train Model
   - Click "Train Model".
   - This will train the machine learning model on the data you collected.
   - A success message will appear when done.

### 3. Sign to Text
   - Click "Sign to Text".
   - The camera will open.
   - Make the signs you trained, and the text will appear on the screen!

### 4. Text to Sign
   - **Important**: You need images for this feature.
   - Create a folder named `assets` in this directory.
   - Download ASL images for letters A-Z (e.g., from Kaggle or Google Images).
   - Save them as `A.jpg`, `B.jpg`, etc., inside the `assets` folder.
   - Click "Text to Sign" and enter text to see the corresponding sign language images.

## Where to get Real Sign Language Images?

The app currently uses **placeholder images** (black background with letters) because I cannot download external datasets for you. 

To get real images:
1.  **Download this dataset**: [ASL Alphabet on Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) (or any other ASL dataset).
2.  **Extract the images**: You will see folders like `A`, `B`, `C`... or files like `A.jpg`.
3.  **Copy them to the `assets` folder**:
    -   Take one good image for 'A', rename it to `A.jpg`, and put it in `miniproject/assets`.
    -   Do the same for B-Z.
    -   The app will automatically use your new images next time you run it!

## Troubleshooting
- If `pip` is not recognized, try `python -m pip install ...`
- If camera doesn't open, make sure no other app is using it.
