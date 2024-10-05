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

def get_year_10_data():
    """
    get year 10 assessment data from the user"
    """ 

    print("Please enter the student assessment data from the end of Year 10.")
    print("Data should be first name, target grade, and nine values. All information should be separated by commas and a space.")
    print("Example: Bambi, 7, 20, 46, 32, 54, 76, 49, 59, 47, 60 \n")

    data_str = input("Enter your data here:\n")
    
    assessment_data = data_str.split(",")
    validate_data(assessment_data)


def validate_data(values):
    """
    Inside the try, converts only numeric values entered by user to integers. 
    Raises a ValueError message if total number of values does not equal 11.
    Raises another ValueError if total number of numeric values does not equal 10.
    """
    try:
        [int(word) for word in values if word.isdigit()]
        
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
        
        print("All inputs are valid.")
        
        # if len(values) != 10:
        #     raise ValueError(
        #         f"Exactly 10 numeric values required. You entered {len(data)}"
        #     )

    except ValueError as e:
        print(f"Invaid data: {e}. Please try again. \n")

get_year_10_data()