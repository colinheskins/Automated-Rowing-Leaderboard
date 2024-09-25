from flask import Flask, request
import gspread
import httpx
from datetime import datetime
import os

app = Flask(__name__)


"""
This function receives an authorization code from a GET request,
exchanges it for an access token and uses that to fetch the user's information.
It then posts the new user's details to a Google Sheets document.
"""
@app.route('/authorizationCode', methods=['GET'])
def authorizationCode():
  authorization_code = request.args.get('code')
  try:
    link = f"https://{os.environ["link"]}/authorizationCode"
    data = {
        "client_id": os.environ['client_id'],
        "client_secret": os.environ['client_secret'],
        "grant_type": "authorization_code",
        "redirect_uri": link,
        "code": authorization_code,
        "scope": "user:read,results:write"
    }

    # Make the POST request to the token endpoint
    with httpx.Client() as client:
      response = client.post(
          "https://log.concept2.com/oauth/access_token",
          data=data,
          headers={"Content-Type": "application/x-www-form-urlencoded"})
      # Check if the request was successful (status code 200)
      token = response.json().get("access_token")
    user_info = getUserInfo(token)
    name = user_info.get("first_name", "") + " " + user_info.get(
        "last_name", "")
    concept2_id = user_info.get("id", "")

    post_new_user(name, concept2_id, token)
    return f"Authorization Received, You may close this window now.", 200
  except Exception as e:
    return f"Error retrieving authorization from user. Please click the link in the email and try again: {e}", 400




"""
This function is designed to handle POST requests with JSON payloads associated
with workout data. It processes 'result-added' webhook events and posts
the workout information to a Google Sheets document.
"""
@app.route('/workout', methods=['POST'])
def workout():
  try:
    data = request.json
    event_type = data.get('type')

    if event_type == 'result-added':
      handle_workout(request.json)
    else:
      # Ignore webhook for other event types
      return f'Ignored: {event_type}', 200

    return data, 200
  except Exception as e:
    print(f"error: {e}")
    return f"Error: {e}", 400

"""
Converts a time in seconds to a formatted string "HH:MM:SS".
"""
def convert_seconds_to_time(seconds):
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60

  time_format = "{:1d}:{:02d}:{:02d}".format(int(hours), int(minutes),
                                             int(seconds))
  return time_format

"""
Extracts workout data from a result array and posts it to a Google Sheets document.
"""
def handle_workout(result):
  data = result
  user_id = data["result"]["user_id"]
  distance = data["result"]["distance"]
  seconds = data["result"]["time"] / 10
  try:
    time = convert_seconds_to_time((seconds))
  except Exception:
    time = "00:00:00"

  post_workout(id=user_id, distance=distance, time=time, seconds=seconds)

"""Creates a spreadsheet object of given index and returns worksheet object"""
def get_spreadsheet(sheetNumber):
  sheet_key = os.environ['sheetKey']
  try:
    gc = gspread.service_account(filename= os.environ["filename"] + ".json")
    sheet = gc.open_by_key(sheet_key)
    worksheet = sheet.get_worksheet(sheetNumber)
    return worksheet
  except:
    return "error5", 400

"""
    Posts workout data including user ID, distance, time spent, and seconds
    to different columns in a Google Sheets document.
"""
def post_workout(id, distance, time, seconds):
  # Get the short name from the second sheet (index 1)
  roster_worksheet = get_spreadsheet(2)
  roster_cell = roster_worksheet.find(str(id))
  short_name = roster_worksheet.cell(roster_cell.row, 3).value

  # Get the main sheet (index 0)
  main_worksheet = get_spreadsheet(0)

  # Find the next available row in column A
  next_empty_row = len(main_worksheet.col_values(1)) + 1 if len(
      main_worksheet.col_values(1)) > 0 else 1

  # Update columns in the next empty row
  main_worksheet.update_cell(next_empty_row, 1, short_name)
  main_worksheet.update_cell(next_empty_row, 2, get_date())
  main_worksheet.update_cell(next_empty_row, 3, distance)
  main_worksheet.update_cell(next_empty_row, 4, time)  # Use time directly
  main_worksheet.update_cell(next_empty_row, 5, "Practice")
  main_worksheet.update_cell(next_empty_row, 6, str(seconds))

"""
Adds a new user's details to a Google Sheets document. Details include the user's
name, Concept2 ID, and access token.
"""
def post_new_user(name, concept2_id, token):
  roster = get_spreadsheet(2)

  # Find the next available row in column A
  next_empty_row = len(roster.col_values(1)) + 1

  # Update variables in the same row
  roster.update_cell(next_empty_row, 1, name)
  roster.update_cell(next_empty_row, 2, str(concept2_id))
  roster.update_cell(next_empty_row, 3, str(token))

"""
Retrieves user information from the Concept2 logbook API using an access token.
Returns a dictionary with the user data.
"""
def getUserInfo(token):
  with httpx.Client() as client:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Make the HTTP GET request to retrieve user information
    response = client.get(f"https://log.concept2.com/api/users/me",
                          headers=headers)

    return response.json().get("data")

"""
Returns the current date formatted as "MM/DD/YYYY".
"""
def get_date():
  # Get the current date and time
  current_datetime = datetime.now()

  # Format the date as MM/DD/YYYY
  formatted_date = current_datetime.strftime("%m/%d/%Y")

  return formatted_date



