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
    print("Data should be first name, target grade, and nine values. All information should be separated by commas.")
    print("Example: Bambi, 7, 20, 46, 32, 54, 76, 49, 59, 47, 60 \n")

    data_str = input("Enter your data here:\n")
    
    assessment_data = data_str.split(",")
    validate_data(assessment_data)


def validate_data(values):
    """
    Inside the try, raises a ValueError message if number of values does not equal 11
    """
    try:
        if len(values) != 11:
            raise ValueError(
                f"Exactly 11 values required. You entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invaid data: {e}. Please try again. \n")

get_year_10_data()