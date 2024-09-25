This project is a Flask web application that integrates with Google Sheets to manage user authorization and workout data. It leverages OAuth2 for user authentication, interacts with the Concept2 Logbook API, and updates Google Sheets with user and workout information.

Table of Contents
Features
Prerequisites
Installation
Configuration
Running the Application
API Endpoints
Project Structure
Troubleshooting
License
------------------------------------------------------------------
Features
User Authorization: Handles OAuth2 authorization flow to authenticate users.
Workout Data Handling: Receives and processes workout data via webhooks.
Google Sheets Integration: Stores user and workout information in Google Sheets.
Modular Codebase: Clean and organized code for easy maintenance and scalability.
Prerequisites
Before you begin, ensure you have met the following requirements:

Google Cloud Account to set up Google Sheets API and service account credentials.
Concept2 Logbook API Credentials (client ID and client secret).

------------------------------------------------------------------
Installation
Follow these steps to set up the project locally.

Clone the Repository

bash
Copy code
git clone the link to this repo. I forgot what it was :|
cd flask-google-sheets-integration
Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy code
install the required packages manually:

bash
Copy code
pip install Flask gspread httpx
Configuration


1. Google Sheets API Setup
To interact with Google Sheets, you need to set up a service account and obtain the necessary credentials.

Create a Service Account:

Go to the Google Cloud Console.
Create a new project or select an existing one.
Navigate to IAM & Admin > Service Accounts.
Click Create Service Account.
Provide a name and description, then click Create.
Assign the Editor role or a role with sufficient permissions, then click Continue.
Click Done.
Create and Download JSON Key:

In the Service Accounts list, select your service account.
Navigate to the Keys tab.
Click Add Key > Create New Key.
Choose JSON and click Create.
Save the downloaded JSON file in the project directory.
Share Google Sheet with Service Account:

Open your Google Sheet.
Click Share.
Add the service account's email (found in the JSON file) with Editor permissions.
2. Environment Variables
Create a .env file in the project root directory to store environment variables securely.

bash
Copy code
touch .env
Add the following variables to the .env file:

env
Copy code
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development  # Change to 'production' in a production environment
LINK=https://yourdomain.com  # Replace with your actual domain

# OAuth2 Credentials
CLIENT_ID=your_concept2_client_id
CLIENT_SECRET=your_concept2_client_secret

# Google Sheets Configuration
SHEET_KEY=your_google_sheet_key  # Found in the Google Sheets URL
FILENAME=your_service_account_filename  # Without .json extension

# Optional: Define PORT if not using the default
PORT=5000
Note: Replace placeholder values (your_concept2_client_id, etc.) with your actual credentials.

3. Loading Environment Variables
Ensure that your application loads environment variables. You can use the python-dotenv package for this.

Install python-dotenv:

bash
Copy code
pip install python-dotenv
Modify Your app.py to Load .env:

At the beginning of your app.py, add:

python
Copy code
from dotenv import load_dotenv
load_dotenv()
Running the Application
Start the Flask development server using the following command:

bash
Copy code
flask run
Alternatively, you can run the app directly:

bash
Copy code
python app.py
The application will be accessible at http://localhost:5000 unless you have configured a different port.

API Endpoints
1. /authorizationCode [GET]
Handles OAuth2 authorization by exchanging an authorization code for an access token and storing user details in Google Sheets.

Parameters:

code (string): Authorization code received from the OAuth2 provider.
Response:

200 OK with a success message if authorization is successful.
400 Bad Request with an error message if something goes wrong.
Example Request:


Copy code
GET https://yourdomain.com/authorizationCode?code=AUTH_CODE_HERE
This can be obtained through the developer portal on the concept2 website. Reach out to me at cmheskins@icloud.com for more details.

2. /workout [POST]
Receives workout data via webhook events and updates Google Sheets accordingly.

Request Body:

json
Copy code
{
  "type": "result-added",
  "result": {
    "user_id": "12345",
    "distance": 5000,
    "time": 3600
  }
}
Response:

200 OK with the received data if the event type is handled.
200 OK with an ignored message for other event types.
400 Bad Request with an error message if something goes wrong.
Example Request:

bash
Copy code
POST https://yourdomain.com/workout
Content-Type: application/json

{
  "type": "result-added",
  "result": {
    "user_id": "12345",
    "distance": 5000,
    "time": 3600
  }
}
Project Structure
bash
Copy code
flask-google-sheets-integration/
├── app.py
├── requirements.txt
├── .env
├── service_account.json
└── README.md
app.py: Main Flask application containing routes and logic.
requirements.txt: Python dependencies.
.env: Environment variables (should be excluded from version control).
service_account.json: Google Sheets API credentials (should be excluded from version control).
README.md: Project documentation.
Troubleshooting
Common Issues:

Invalid Credentials:

Ensure that CLIENT_ID, CLIENT_SECRET, and Google Sheets credentials are correct.
Google Sheets Permission Denied:

Verify that the service account email has been granted access to the Google Sheet.
Environment Variables Not Loaded:

Make sure the .env file exists and is correctly formatted.
Confirm that python-dotenv is installed and loaded in app.py.
Port Already in Use:

Change the port in the .env file or terminate the process using the port.
Logging:

Check the console output for error messages.
Implement additional logging as needed for deeper insights.
License
This project is licensed under the MIT License.