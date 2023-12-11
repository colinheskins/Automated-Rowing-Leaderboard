from google.oauth2.service_account import Credentials
import gspread
import asyncio
import helpers
from datetime import timedelta,datetime


logger = helpers.get_logger()

#creates worksheet object
async def get_spreadsheet(sheetNumber):
    try:
        gc = gspread.service_account(filename="D:\donlods\saintx-rowing-8c078656a295.json")
        sheet = gc.open_by_key("1UwRda-4VLryrdWkvnM99HMO_y0Lt78ek8WkV30WWXVw")
        worksheet = sheet.get_worksheet(sheetNumber)
        return worksheet
    except Exception as e:
        logger.critical(f"Error creating spreadsheet object. Error: {e}")


#adds distance to value in spreadsheet if name already exists, else add name and distance in new row
async def post_to_spreadsheet(name, distance, time):
    try:
        currentTime  = await helpers.get_time()
        roster_worksheet = await get_spreadsheet(1)  # Assuming sheet2 is at index 1
        roster_cell = roster_worksheet.find(name)
        shortened_name = roster_worksheet.cell(roster_cell.row, 2).value

        # Get the main sheet (sheet1)
        main_worksheet = await get_spreadsheet(0)

        # Update columns A, B, C, D in the next empty row
        next_empty_row = len(main_worksheet.col_values(1)) + 1  # Find the next empty row in column A

        # Update columns A, B, C, D in the next empty row
        main_worksheet.update_cell(next_empty_row, 1, shortened_name)
        main_worksheet.update_cell(next_empty_row, 2, currentTime)
        main_worksheet.update_cell(next_empty_row, 3, distance)
        main_worksheet.update_cell(next_empty_row, 4, time)
    except Exception as e:
        logger.critical(f"Error updating spreadsheet. Error: {e}")
