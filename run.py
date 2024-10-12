import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('the_fairytale_school_of_mfl')
DATA_RANGE = 'B3:J3'

def get_year_10_data():
    """
    Get year 10 assessment data from the user.
    Run a while loop to collect valid data from the user that must consist of a name followed by 10 integers, each separated by a comma and a space. The request will continue to run until valid data is collected.
    """ 
    while True: # Repeats user input request when invalid data is input.
        print("Please enter the student assessment data from the end of Year 10.")
        print("Data should be first name, target grade, and nine values. All information should be separated by commas only, no space.")
        print("Example: Bambi, 7, 20, 46, 32, 54, 76, 49, 59, 47, 60 \n")

        data_str = input("Enter your data here:\n")
    
        assessment_data = data_str.split(",")
    
        if validate_data(assessment_data):
            print("All inputs are valid.")
            break

    return assessment_data

def validate_data(values):
    """
    Inside the try, converts only numeric values entered by user to integers. 
    Raises a ValueError message if total number of values does not equal 11.
    Raises another ValueError if first value input is not a name.
    Raises another ValueError if values 2-11 are not numbers.
    """
    try:
        [int(item) if item.isdigit() else item for item in values] # Converts only numeric inputs into integers
        
        if len(values) != 11:
            raise ValueError(
                f"Exactly 11 total values required. You entered {len(values)}"
            )

        # Check if the first input is a name (string without numbers)
        if not values[0].isalpha():
            raise ValueError("The first input must be a name (letters only)")
        
        # Check if inputs 2-11 are numbers
        for i in range(1, 10):
            try:
                float(values[i])  # This will check if the user input can be converted to a float
            except ValueError:
                raise ValueError(f"Input {i+1} must be a number.")
        

    except ValueError as e:
        print(f"Invalid data: {e}. Please try again. \n")
        return False

    return True

def update_assessment_data(data):
    """
    Update assessment data worksheet, adding a new row with the list data provided.
    """

    print("Updating Assessment Worksheet ... \n")
    assessment_worksheet = SHEET.worksheet("year 10 data") #access year 10 data worksheet
    assessment_worksheet.append_row(data) #update year 10 data worksheet with user data
    print("Assessment Worksheet successfully updated.\n")

def calculate_average(assessment_data):
    """
    Open specified worksheet to access data from.
    Calculate average percentage per column based on all data in spreadsheet.
    Update 'median' worksheet with average percentages by module of study.
    """

    print("Calculating average percentage data ...")
    # Open the year 10 data spreadsheet 
    data_sheet = SHEET.worksheet('year 10 data')

    # Get all values from the worksheet
    all_values = data_sheet.get_all_values()

    # Initialize list to store averages
    averages = []

    # Iterate over each column index to target specific data for calculation
    for col_index in range(2, 11):
        column_values = [int(row[col_index]) for row in all_values if row[col_index].isdigit()]
        if column_values:
            average = sum(column_values) / len(column_values) #calculate average percentage for input in spreadsheet
            whole_number_average = round(average) #round average to a whole number
            averages.append(whole_number_average)
        else:
            averages.append(0)
    return averages


def update_median_worksheet(averages_data):
    """
    Update median % worksheet with average percentages calculated per module and exam.
    """

    median_worksheet = SHEET.worksheet('median %')
    # Update the 'median' worksheet with the average percentage per module/assessment
    median_worksheet.append_row(averages_data)

    print('Average percentages updated in median % worksheet.')

def find_lowest_module_value(averages_data):
    median_data = SHEET.worksheet('median %')

    median_values = median_data.get_all_values()

    lowest_module_value = []

    for col_index in range(0,5):
        column_values = [int(row[col_index]) for row in median_values if row[col_index].isdigit()]
        if column_values:
            module_value = min(column_values)
            lowest_module_value.append(module_value)
        return module_value

    print("Module to be revised is:", lowest_module_value)
    

def main():
    data = get_year_10_data()
    assessment_data = [int(item) if item.isdigit() else item for item in data]
    update_assessment_data(assessment_data)
    averages_data = calculate_average(assessment_data)
    update_median_worksheet(averages_data)
    find_lowest_module_value(averages_data)

print("Welcome to The Fairytale School of MFL's data automation programme:")
main() 