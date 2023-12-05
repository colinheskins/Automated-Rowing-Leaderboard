import json
import concept2
import asyncio
import worksheet
import logging 
import helpers
import authCode

async def main():
    json_filename = 'users.json'
    logger = helpers.get_logger()
    #token1 = await authCode.startAuth() #just test, ignore: has no use
    try:
        with open(json_filename, 'r') as json_file:
            user_data = json.load(json_file)

        for user in user_data.get("users", []):
            token = user.get('accessToken')
            name = user.get('name')
            user_info = await concept2.getUserInfo(token)
            if user_info:
                distances,time = await concept2.get_results(token)
                logger.info(f"Processing user: {name} with distances: {distances}")
                await worksheet.post_to_spreadsheet(name, distances)
            else:
                logger.error(f"Error getting user information for token: {token}")
    except FileNotFoundError:
        logger.critical(f"Error: JSON file '{json_filename}' not found.")
    except Exception as e:
        logger.error("Error")

asyncio.run(main())
