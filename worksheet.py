from google.oauth2.service_account import Credentials
import gspread
import asyncio
import helpers

logger = helpers.get_logger()

#creates worksheet object
async def get_spreadsheet_leaderboard():
    try:
        gc = gspread.service_account(filename="D:\donlods\saintx-rowing-8c078656a295.json")
        sheet = gc.open_by_key("1HRqRXwVddUr_EfFQLfKMOa-U1m7-HYsYFt-uetcbCaY")
        worksheet = sheet.get_worksheet(0)
        return worksheet
    except Exception as e:
        logger.critical(f"Error creating spreadsheet object. Error: {e}")


#adds distance to value in spreadsheet if name already exists, else add name and distance in new row
async def post_to_spreadsheet(name, distance):
    try:
        worksheet = await get_spreadsheet_leaderboard()

        # Get all values in column A
        names_column = worksheet.col_values(1)

        # Check if the combination of first name and last name exists
        full_name = name
        if full_name not in names_column:
            # If the name doesn't exist, find the next available row
            next_row = len(names_column) + 1

            # Add the information to the next available row
            worksheet.update_cell(next_row, 1, full_name)  # Update column A
            worksheet.update_cell(next_row, 2, distance)  # Update column B
        else:
            # If the name already exists, find its row index
            row_index = names_column.index(full_name) + 1

            # Get the current value in the corresponding cell
            current_value = worksheet.cell(row_index, 2).value
            if current_value is None:
                current_value = 0

            # Convert the current value to a numeric type (assuming it's a number)
            try:
                current_value_numeric = float(current_value)
            except ValueError:
                # Handle the case where the current value is not a valid number
                current_value_numeric = 0

            # Add the new distance to the current value
            new_total_distance = current_value_numeric + distance

            # Update the corresponding row in column B with the new total distance
            worksheet.update_cell(row_index, 2, new_total_distance)
    except Exception as e:
        logger.error(f"Error writing to spreadsheet: {e}")


