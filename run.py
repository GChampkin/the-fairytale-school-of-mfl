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
    Run a while loop to collect valid data from the user.
    The request will continue to run until valid data is collected.
    """
    while True:  # Repeats user input request when invalid data is input.
        print("Please enter the student assessment data. \n")
        print("Data should be: name, target grade, and nine values(%): \n")
        print("Modules 1-5 \n")
        print("Reading Mock \n")
        print("Listening Mock \n")
        print("Writing Mock \n")
        print("Speaking Mock. \n")
        print("""Data should be separated by commas only, no space. \n""")
        print("Example: Bambi,7,20,46,32,54,76,49,59,47,60 \n")

        data_str = input("Enter student data here:\n")

        assessment_data = data_str.split(",")

        if validate_data(assessment_data):
            print("All inputs are valid. \n")
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
        # Converts only numeric inputs into integers.
        [int(item) if item.isdigit() else item for item in values]

        if len(values) != 11:
            raise ValueError(
                f"Exactly 11 values required. You entered {len(values)} \n"
            )

        # Ensure first input is a name for correct input in the spreadsheet.
        if not values[0].isalpha():
            raise ValueError("The first input must contain letters only \n")

        # Check if inputs 2-11 specifically are numbers.
        for i in range(1, 10):
            try:
                float(values[i])
            except ValueError:
                raise ValueError(f"Input {i+1} must be a number. \n")

    except ValueError as e:
        print(f"Invalid data: {e}Please try again. \n")
        return False

    return True


def update_assessment_data(data):
    """
    Update assessment data worksheet.
    Add a new row with the list data provided.
    """

    print("Updating Assessment Worksheet ... \n")
    # access year 10 data worksheet
    # update year 10 data worksheet with user data
    assessment_worksheet = SHEET.worksheet("year 10 data")
    assessment_worksheet.append_row(data)
    print("Assessment Worksheet successfully updated.\n")


def calculate_average(assessment_data):
    """
    Open specified worksheet to access data from.
    Calculate average percentage per column based on all data in spreadsheet.
    Update 'median' worksheet with average percentages by module of study.
    """

    print("Calculating average percentage data ... \n")
    # Open the year 10 data spreadsheet to access data.
    data_sheet = SHEET.worksheet('year 10 data')

    # Get all values from the worksheet to calculate average.
    all_values = data_sheet.get_all_values()

    # Initialize list to store averages to run through next function.
    averages = []

    # Iterate over specific column index
    for col_index in range(2, 11):
        column_values = [
            int(row[col_index])
            for row in all_values
            if row[col_index].isdigit()
        ]
        if column_values:
            # calculate average percentage
            average = sum(column_values) / len(column_values)
            # round to a whole number for input in spreadsheet.
            whole_number_average = round(average)
            averages.append(whole_number_average)
        else:
            averages.append(0)
    return averages


def update_median_worksheet(averages_data):
    """
    Update median % worksheet with average percentages per module and exam.
    """

    print("Updating averages in median % worksheet ... \n")
    median_worksheet = SHEET.worksheet('median %')
    median_worksheet.append_row(averages_data)

    print('Average percentages updated in median % worksheet. \n')


def find_lowest_values(averages_data):
    """
    Get lowest value from module assessment averages and return module.
    Get lowest value from exam skill assessment averages and return skill.
    """
    median_data = SHEET.worksheet('median %')

    median_values = median_data.get_all_values()

    results = []
    # Find lowest module value of averages data to target foci.
    lowest_value_module = min(median_values[-1][:5])
    # Get index of lowest module value to track column heading.
    min_indices_module = [
        i
        for i, x in enumerate(median_values[-1][:5])
        if x == lowest_value_module
    ]

    for index in min_indices_module:
        # Get top cell value dependent on index of lowest module value.
        module_index = median_values[0][index]
        # Stores sourced top column value to store in container.
        results.append(module_index)

    # Find lowest skill value of averages data to target foci.
    lowest_value_skill = min(median_values[-1][5:9])
    # Find index of lowest skill value for same purpose as line 132.
    min_indices_skill = [
        i + 5
        for i, x in enumerate(median_values[-1][5:9])
        if x == lowest_value_skill
    ]

    for index in min_indices_skill:
        # Get top cell value dependent on index of lowest skill value.
        skill_index = median_values[0][index]
        results.append(skill_index)

    return results


def update_foci_worksheet(results):
    """
    Update foci worksheet with lowest values for intervention.
    """

    print("Updating foci in foci worksheet ... \n")
    foci_worksheet = SHEET.worksheet('foci')
    # Update foci worksheet with results data for confirmation to user.
    foci_worksheet.append_row(results)
    print("Foci worksheet updated. \n")


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
    # Print to terminal required module and skill focus for interention.
    print("Module to be revised:", "".join(results[0]), "\n")
    print("Skill to be revised:", "".join(results[1]), " \n")


print("Welcome to The Fairytale School of MFL's Intervention Identifier: \n")
main()
print("Good luck for the exams!")
