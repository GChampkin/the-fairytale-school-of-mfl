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
DATA_SHEET_ID = '158HIpT7YzfjL9MT2PbcCzGQjRFRUrVgeu0RPqmUtyHM'
DATA_RANGE = 'A17:K17'

def get_year_10_data():
    """
    Get year 10 assessment data from the user.
    Run a while loop to collect valid data from the user that must consist of a name followed by 10 integers, each separated by a comma and a space. The request will continue to run until valid data is collected.
    """ 
    while True: # Repeats user input request when invalid data is input.
        print("Please enter the student assessment data from the end of Year 10.")
        print("Data should be first name, target grade, and nine values. All information should be separated by commas and a space.")
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
        print(values)
        
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
        print(f"Invaid data: {e}. Please try again. \n")
        return False

    return True

def update_assessment_data(data):
    """
    Update assessment data worksheet, adding a new row with the list data provided.
    """

    print("Updating Assessment Worksheet ... \n")
    assessment_worksheet = SHEET.worksheet("year 10 data") #access year 10 data worksheet
    assessment_worksheet.update([data], DATA_RANGE) #update year 10 data worksheet with user data
    print("Assessment Worksheet successfully updated.\n")

def calculate_average():
    """
    Open specified worksheet to access data from.
    Calculate average percentage per column based on all data in spreadsheet.
    Update 'median' worksheet with average percentages by module of study.
    """
    # Open the spreadsheet and the specific worksheets
    data_sheet = SHEET.worksheet('year 10 data')
    median_sheet = SHEET.worksheet('median %')

    # Retrieve all data from the data sheet
    data = data_sheet.get_all_values()

    # Convert the data to a list of lists, removing any empty strings
    data_values = [[float(cell) for cell in row[2:] if cell] for row in data[2:] if row]
    print(data_values)
    # Calculate the average percentage of data
    # total_values = sum(len(column) for column in data_values)
    # total_cells = len(data) * len(data[0])  # Assuming the sheet is a complete rectangle
    # average_percentage = (total_values / total_cells) * 100 # calculate average percentage

    # # Update the 'median' worksheet with the average percentage per module/assessment
    # median_sheet.update('B3:J3')

    # print('Average percentages updated in median % worksheet.')

def main():
    data = get_year_10_data()
    assessment_data = [int(item) if item.isdigit() else item for item in data]
    update_assessment_data(assessment_data)
    calculate_average()

print("Welcome to The Fairytale School of MFL's data automation programme:")
main() 