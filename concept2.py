import httpx
import logging
import asyncio
import os
import json
import authCode
import logging
from loggingz import logs
import helpers

API_BASE_URL = "https://log.concept2.com"
logger = helpers.get_logger()


# Run the event loop to execute the coroutine

async def access_token():
  auth = await authCode.startAuth()
  #print(auth)
  try:
      with httpx.Client() as client:
          headers = {}
          get_params = {
            "client_id" : helpers.client_id,
            "client_secret" : helpers.client_secret,
            "grant_type" : "authorization_code",
            "scope" : "results:read,results:right,results:write",
            "code" : auth,
            "redirect_uri" : "http://localhost:5000/callback"
          }
          response = client.post(
            f"{API_BASE_URL}/oauth/access_token",
              data=get_params
          )
          if response.status_code == httpx.codes.ok:
            code = response.json().get("access_token")
            await add_user_to_json(code)
            return code
          else:
            logger.warning(f"Failed to retrieve data from Concept2 API. HTTP Error {response.status_code} ")
  except Exception as e:
      logger.error(f"Error retrieving access code from authorization grant: {e}")


async def get_results(token):
    try:
        with httpx.Client() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            # Example: Get all rower results in xxx
            params = {
                "updated_after": '2013-06-21',#await helpers.get_time(),
                "type": "rower",
            }

            response = client.get(
                f"{API_BASE_URL}/api/users/me/results",
                headers=headers,
                params=params
            )

            if response.status_code == httpx.codes.ok:
                print("Results retrieved successfully!")
                workouts = response.json()['data']
                return [workout.get('distance', 0) for workout in workouts]
                
            else:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)

    except Exception as e:
        print(f"Error getting results: {e}")


async def getUserInfo(token):
    try:
        with httpx.Client() as client:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            # Make the HTTP GET request to retrieve user information
            response = client.get(
                f"{API_BASE_URL}/api/users/me", 
                headers=headers
            )

            user_info = response.json().get("data")
            return user_info
    except httpx.HTTPStatusError as e:
      logger.error(f"HTTP Error({response.status_code}) in method getUserInfo for token {token}: {e}" )
    except Exception as e:
      logger.error(f"Error getting user information for token {token}: {e}")

async def add_user_to_json(token):
    fileName = "users.json"
    user_info = await getUserInfo(token)
    name = user_info.get("first_name", "") + " " + user_info.get("last_name", "")
    try:
        # Load existing data from the JSON file
        with open(fileName, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        json_data = {"users": []}

    # Check if the user already exists in the data
    user_exists = any(user["accessToken"] == token for user in json_data["users"])

    # If the user doesn't exist, add a new entry
    if not user_exists:
        new_user = {"accessToken": token, "name": name}
        json_data["users"].append(new_user)

        # Save the updated data back to the JSON file
        with open(fileName, 'w') as file:
            json.dump(json_data, file, indent=2)
        logger.info(f"User {name} added successfully.")
    else:
        logger.info(f"User {name} already exists.")



