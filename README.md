# Audio Processing App with Vapor and PythonKit

## Introduction
This app is designed to upload, list, and process audio files using a Vapor backend and Python scripts. It allows users to upload audio files in .mp3 or .wav formats, list uploaded files, and process them to extract text using Python's audio-to-text libraries. This integration showcases the power of combining Swift's Vapor framework with Python's extensive library ecosystem for audio processing tasks.

## Setup

### Prerequisites
- Swift 5.9
- Vapor 4.92.4
- Python 3.12
- PythonKit
- Google Cloud Developer Account

### Installation
1. Clone this repository to your local machine.
2. Ensure you have Python 3 installed and accessible from your terminal.
3. Install Vapor if you haven't already. You can find instructions at [Vapor's official documentation](https://docs.vapor.codes/4.0/install/macos/).
4. Navigate to the project directory and run `swift build` to compile the project.
5. Ensure the required Python packages are installed:
   - Navigate to the `AudiotoText` directory within the project.
   - Run `pip3 install -e .` to install the Python package and its dependencies.

## Running the App
1. Start the app by running `swift run` from the command line within the project directory.
2. The app will start running on `localhost:8080`.
3. Use a tool like Postman or curl to interact with the app's endpoints:
   - POST `/upload` to upload audio files.
   - GET `/list` to list all uploaded audio files.
   - POST `/process` to process an uploaded audio file and extract text.
4. Make sure to Google Developer account key and Audio-to-text api is enabled.

## Features
- **File Upload**: Users can upload audio files through the `/upload` endpoint. The app supports `.mp3` and `.wav` file formats.
- **List Audio Files**: The `/list` endpoint provides a list of all uploaded audio files.
- **Audio Processing**: The `/process` endpoint takes uploaded audio files and uses a Python script to convert audio to text. It demonstrates integrating Python functionality into a Vapor app through PythonKit.

## Google Cloud Setup for Speech-to-Text API

### Creating a Google Developer Account
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. If you don't already have a Google account, you will need to create one.
3. Once logged in, you may be prompted to agree to the Terms of Service, choose whether to receive email updates, and agree to the terms of the free trial, if applicable.

### Creating a New Project
1. In the Google Cloud Console, select or create a new project by clicking on the project name at the top of the page next to "Google Cloud Platform".
2. Click on "New Project", give it a name, and note the Project ID. You'll need it later.

### Enabling the Speech-to-Text API
1. With your project selected, navigate to the "APIs & Services" dashboard.
2. Click on "ENABLE APIS AND SERVICES" to view the API Library.
3. Search for "Speech-to-Text API" and select it.
4. Click "ENABLE" to enable the Speech-to-Text API for your project.

### Setting Up Authentication
1. In the "APIs & Services" dashboard, go to the "Credentials" tab.
2. Click "Create credentials" and select "Service account".
3. Fill in the service account details and grant it the "Project > Owner" role.
4. Once the service account is created, click on it to view its details.
5. Under "Keys", click "Add Key" and choose "Create new key".
6. Select "JSON" as the key type and click "Create". The JSON key file will be downloaded to your computer.

### Configuring Your Application
1. Securely store the downloaded JSON key file in your application's directory. **Do not** commit this file to your version control system.
2. Set an environment variable named `GOOGLE_CLOUD_CREDENTIALS` on your server or development machine that points to the JSON key file. For example, in your terminal:
   ```bash
   export GOOGLE_CLOUD_CREDENTIALS="/path/to/your-service-account-file.json"
   ```

