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
        [int(word) for word in values if word.isdigit()] # Converts only numeric inputs into integers
        
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
                float(values[i])  # This will check if the input can be converted to a float
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
    assessment_worksheet = SHEET.worksheet("year 10 data")
    assessment_worksheet.update([assessment_data], DATA_RANGE)
    print("Assessment Worksheet successfully updated.\n")

def main():
    data = get_year_10_data()
    assessment_data = [int(word) for word in data if word.isdigit()]
    update_assessment_data(assessment_data)

main() 