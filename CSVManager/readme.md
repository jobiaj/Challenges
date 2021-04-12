Requirements:
Python 3.x

Running command:
python CSVDataManager.py {INPUT_FILE_PATH} {CONFIGURATION_FILE_PATH} {OUTPUT_FILE_PATH}
Eg. python CSVDataManager.py test/input/date_format_input.csv test/output/date_format_output.csv test/config/date_format_config.txt

Run Test Cases:
python CSVDataManager.py --test

Help documentation command:
python CSVDataManager.py --help

Configuration details:

1. Date Formatting:

User should enter the following parameters in the configuration file for formatting the date column to another format.
mode:<Provide mode of the configuration file as 'dateformat'>
from:<Provide format of the date in the given CSV File. We are using python for the formating the given date. To check format symbols please check: https://www.w3schools.com/python/python_datetime.asp: Eg. Format:%Y-%m-%d>
to:<Provide format to which you wanted to convert the given date in the CSV File. We are using python for the formating the given date. To check format symbols please check: https://www.w3schools.com/python/python_datetime.asp: Eg. Format:%b %d, %Y>
column:<Provide Column name in the csv file>

Sample configuration file content for the date format.
mode:dateformat
from:%Y-%m-%d
to:%b %d, %Y
column:dob

2. Data Filtering:

mode:<Provide mode of the configuration file as 'filtering'>
column:<Give the column name based on which you wanted to filter the data.>
action:<Provide the action: Available actions are greaterthan, lessthan, greaterthanorequalto, lessthanorequalto, and equalto>
value:<Value to be compared.>

Sample configuration file content for the Data Filtering.
mode:filtering
column:age
action:greaterthan
value:50

3. Combining Multiple Columns:

mode:<Provide mode of the configuration file as 'mergecolumn'>
columns:<Give the column names which you wanted to merge as comma separated string.>
action:<Provide the format of the merged column.>
value:<Provide the new column name.>

Sample configuration file content for Combining Multiple Columns.
mode:mergecolumn
columns:first_name,last_name
merge_format:first_name, last_name
new_column_name:name

4. Creating a new column based on the existing column:

mode:<Provide mode of the configuration file as 'create_new_column'>
new_column:<Provide the new column name.>
check_column:<Provide the name of the column for validating the condition provided.>
value:<Provide the value for comparision statement.>
action:<Provide the action: Available actions are greaterthan, lessthan, greaterthanorequalto, lessthanorequalto, and equalto>
condition_failure_val:<Provide the value on condition failure>
condition_success_val:<Provide the value on condition sucess>

Sample configuration file content for Creating a new column based on the existing column.
mode:create_new_column
new_column:eligible_for_voting
check_column:age
value:18
action:greaterthan
condition_failure_val:F
condition_success_val:T
