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
    Get year 10 assessment data from the user.
    Run a while loop to collect valid data from the user that must consist of a name followed by 10 integers, each separated by a comma and a space. The request will continue to run until valid data is collected.
    """ 
    while True: # Repeats user input request when invalid data is input.
        print("Please enter the student assessment data from the end of Year 10.")
        print("Data should be first name, target grade, and nine values. All information should be separated by commas only, no space.")
        print("Example: Bambi,7,20,46,32,54,76,49,59,47,60 \n")

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
        [int(item) if item.isdigit() else item for item in values] # Converts only numeric inputs into integers as data contains strings and integers.
        
        if len(values) != 11:
            raise ValueError(
                f"Exactly 11 total values required. You entered {len(values)}"
            )

        # Check if the first input is a name (string without numbers) to ensure correct data is input for the spreadsheet.
        if not values[0].isalpha():
            raise ValueError("The first input must be a name (letters only)")
        
        # Check if inputs 2-11 specifically are numbers to verify only requitred data.
        for i in range(1, 10):
            try:
                float(values[i])  # This will check if the user input can be converted to a float required for running calculations.
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
    # Open the year 10 data spreadsheet to access data.
    data_sheet = SHEET.worksheet('year 10 data')

    # Get all values from the worksheet to calculate average.
    all_values = data_sheet.get_all_values()

    # Initialize list to store averages to run through next function.
    averages = []

    # Iterate over each column index to target specific data for calculation
    for col_index in range(2, 11):
        column_values = [int(row[col_index]) for row in all_values if row[col_index].isdigit()]
        if column_values:
            average = sum(column_values) / len(column_values) 
            whole_number_average = round(average) #calculate average percentage and round to a whole number for input in spreadsheet.
            averages.append(whole_number_average)
        else:
            averages.append(0)
    return averages


def update_median_worksheet(averages_data):
    """
    Update median % worksheet with average percentages calculated per module and exam.
    """

    print("Updating averages in median % worksheet ...")
    median_worksheet = SHEET.worksheet('median %')
    median_worksheet.append_row(averages_data) # Update the 'median' worksheet with the average percentage per module/assessment.

    print('Average percentages updated in median % worksheet.')

def find_lowest_values(averages_data):
    """
    Get and return lowest value from module assessment averages.
    Get and return lowest value from exam skill assessment averages.
    """
    median_data = SHEET.worksheet('median %')

    median_values = median_data.get_all_values()

    results = [] # Create container to store foci data for running through update function and printing to terminal.

    lowest_value_module = min(median_values[-1][:5]) # Find lowest module value of averages data on median worksheet to target foci.
    min_indices_module = [i for i, x in enumerate(median_values[-1][:5]) if x == lowest_value_module] # Find index of lowest module value to track column heading for output to the terminal.

    for index in min_indices_module:
        module_index = median_values[0][index] # Find value of cell at top of column dependent on index of lowest module value. 
        results.append(module_index) # Stores sourced top column value to store in container.


    lowest_value_skill = min(median_values[-1][5:9]) # Find lowest skill value of averages data on median worksheet to target foci.
    min_indices_skill = [i + 5 for i, x in enumerate(median_values[-1][5:9]) if x == lowest_value_skill] # Find index of lowest skill value for same purpose as line 132.

    for index in min_indices_skill:
        skill_index = median_values[0][index] # Find value of cell at top of column dependent on index of lowest skill value.
        results.append(skill_index) # Stores sources top column value to store in container.

    return results


def update_foci_worksheet(results):
    """
    Update foci worksheet with lowest values for intervention.
    """

    print("Updating foci in foci worksheet ... ")
    foci_worksheet = SHEET.worksheet('foci') # Access foci worksheet.
    foci_worksheet.append_row(results) # Update foci worksheet with results data for confirmation to user.
    print("Foci worksheet updated.")
    

def main():
    """
    Run all functions to produce desired output. 
    """
    data = get_year_10_data()
    assessment_data = [int(item) if item.isdigit() else item for item in data]
    update_assessment_data(assessment_data)
    averages_data = calculate_average(assessment_data)
    update_median_worksheet(averages_data)
    results = find_lowest_values(averages_data)
    update_foci_worksheet(results)
    print("Module to be revised:", "".join(results[0]))
    print("Skill to be revised:", "".join(results[1])) # Print to terminal required module and skill focus for interention. 

print("Welcome to The Fairytale School of MFL's data automation programme:")
main() 
print("Good luck for the exams!")
