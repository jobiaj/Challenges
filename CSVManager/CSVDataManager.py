import csv
import datetime
import re
import sys
from os import path



def validate_int(int_str, get_string=False):
    try:
        int_str = int(int_str)
    except ValueError:
        if get_string:
            return int_str
        raise RuntimeError("Expected integer value, got string.")
    return int_str

class Configuration(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.mode_dict = None
        self.read_configuration_file_update_mode_info()


    def read_configuration_file_update_mode_info(self):
        with open(self.file_path, 'r') as confg_file:
            lines = confg_file.readlines()
            mode_dict = {}
            for line in lines:
                items = line.split(':')
                mode_dict[items[0]] = items[1].rstrip('\n')
            
        if "mode" not in mode_dict:
            raise RuntimeError("The mode should be there in the configuration file.")
        self.mode_dict = mode_dict

  
    def get_modified_data(self, field_names, dict_list):
        if not self.mode_dict:
            raise RuntimeError("Something went wrong, This doesn't have a proper configuration")
        modified_dict = None
        mode = self.mode_dict['mode']
        if mode.lower() == "dateformat":
            modified_dict = self.convert_data_with_dateformat(dict_list)
        elif mode.lower() == "mergecolumn":
            field_names, modified_dict = self.generate_merged_data(field_names, dict_list)
        elif mode.lower() == "filtering":
            modified_dict = self.filter_data(dict_list)
        elif mode.lower() == "create_new_column":
            field_names, modified_dict = self.generate_new_column(field_names, dict_list)
        else:
            raise RuntimeError("Please provide a valid mode of operation in the configuration file.")

        return field_names, modified_dict


    def generate_new_column(self, field_names, dict_list):
        mode_dict_keys = self.mode_dict.keys()
        new_column = self.mode_dict["new_column"] if "new_column" in mode_dict_keys else None
        check_column = self.mode_dict["check_column"] if "check_column" in mode_dict_keys else None
        value = self.mode_dict["value"] if "value" in mode_dict_keys else None
        action = self.mode_dict["action"] if "action" in mode_dict_keys else None
        condition_failure_val = self.mode_dict["condition_failure_val"] if "condition_failure_val" in mode_dict_keys else None
        condition_success_val = self.mode_dict["condition_success_val"] if "condition_success_val" in mode_dict_keys else None
        if new_column and check_column and value and action and condition_failure_val and condition_success_val:
            for item in dict_list:
                if action == "equalto":    
                    lhs = validate_int(item[check_column],  True)
                    rhs = validate_int(value,  True)
                else:
                    lhs = validate_int(item[check_column])
                    rhs = validate_int(value)
                if action == "greaterthan":
                    item[new_column] = condition_success_val if lhs > rhs else condition_failure_val                
                elif action == "lessthan":
                    item[new_column] = condition_success_val if lhs < rhs else condition_failure_val
                elif action == "lessthanorequalto":
                    item[new_column] = condition_success_val if lhs <= rhs else condition_failure_val 
                elif action == "greaterthanorequalto":
                    item[new_column] = condition_success_val if lhs >= rhs else condition_failure_val
                elif action == "equalto":
                    item[new_column] = condition_success_val if lhs == rhs else condition_failure_val
                else:
                    raise RuntimeError("Invalid action: %s" % action)
            field_names.append(new_column)
        else:
            raise RuntimeError("Please check 'new_column', \
                'check_column', 'value', 'action', 'condition_failure_val' \
                and 'condition_success_val' in the configuration file")
        return field_names, dict_list 

    def filter_data(self, dict_list):
        mode_dict_keys = self.mode_dict.keys()
        column = self.mode_dict["column"] if "column" in mode_dict_keys else None
        action = self.mode_dict["action"] if "action" in mode_dict_keys else None
        value = self.mode_dict["value"] if "value" in mode_dict_keys else None

        if column and action and value:
            action = action.lower()
            if action == "greaterthan":
                dict_list = [x for x in dict_list if validate_int(x[column]) < validate_int(value)]
            elif action == "lessthan":
                dict_list = [x for x in dict_list if validate_int(x[column]) > validate_int(value)]
            elif action == "lessthanorequalto":
                dict_list = [x for x in dict_list if validate_int(x[column]) >= validate_int(value)]
            elif action == "greaterthanorequalto":
                dict_list = [x for x in dict_list if validate_int(x[column]) <= validate_int(value)]
            elif action == "equalto":
                dict_list = [x for x in dict_list if validate_int(x[column], True) == validate_int(value, True)]
            else:
                raise RuntimeError("Invalid action: %s" % action)

        else:
            raise RuntimeError("Please check 'column', 'action' and 'value' in the configuration file")
        return dict_list           


    def generate_merged_data(self, field_names, dict_list):
        mode_dict_keys = self.mode_dict.keys()
        merge_columns = self.mode_dict["columns"] if "columns" in mode_dict_keys else None
        merge_format = self.mode_dict["merge_format"] if "merge_format" in mode_dict_keys else None
        new_column_name = self.mode_dict["new_column_name"] if "new_column_name" in mode_dict_keys else None
        
        if merge_columns and merge_format and new_column_name:
            to_be_merged = merge_columns.split(',')
            for item in dict_list:
                new_data = merge_format
                for column in to_be_merged:
                    new_data = new_data.replace(column, item[column])
                    item.pop(column, None)
                item[new_column_name] = new_data
            for column in to_be_merged:
                field_names.remove(column)
            field_names.append(new_column_name)
        else:
            raise RuntimeError("Please check 'columns', 'merge_format' and 'new_column_name' in the configuration file")
        return field_names, dict_list          
    


    def convert_data_with_dateformat(self, dict_list):
        mode_dict_keys = self.mode_dict.keys()
        from_format = self.mode_dict["from"] if "from" in mode_dict_keys else None
        to_format = self.mode_dict["to"] if "to" in mode_dict_keys else None
        column = self.mode_dict["column"] if "column" in mode_dict_keys else None

        if to_format and from_format and column:
            for item in dict_list:
                to_be_changed = item[column]
                try:
                    changed_data = datetime.datetime.strptime(to_be_changed, from_format).strftime(to_format)
                except Expection as e:
                    raise RuntimeError("Failed to convert data %s in %s format to %s format" %(to_be_changed, from_format, to_format))

                item[column] = changed_data
        else:
            raise RuntimeError("Please check 'column', 'from' and 'to' in the configuration file")
        return dict_list



class CSVManager(object):
    
    def __init__(self, input_path, output_path, configuration_path):
        self.input_path = input_path
        self.configuration = Configuration(configuration_path)
        self.output_path = output_path


    def write_to_csv(self, csv_dicts, field_names):
        with open(self.output_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = '|')
            writer.writerow(field_names)
            for csv_row in csv_dicts:
                writer.writerow(csv_row.values())


    def read_csv_file(self):
        with open(self.input_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = '|')
            dict_list = []
            for line in reader:
                line_list = list(line.items())
                dict_list.append({x[0]: x[1] for x in line_list})
            field_names = reader.fieldnames
        return field_names, dict_list

    def generate_csv_based_on_configuration(self):
        field_names, dict_list = self.read_csv_file()
        field_names, dict_list = self.configuration.get_modified_data(field_names, dict_list)
        if not dict_list:
            raise RuntimeError("Failed to generate new CSV Data.")
        self.write_to_csv(dict_list, field_names)
        return "Data Generated successfully. View the file at: %s" % self.output_path



def get_testcases():
    testcase_dict = {"Date Format": [{"name": "Date Format: Convert date in %Y-%m-%d to %b %d, %Y",
                      "input": "test/input/date_format_input.csv", 
                      "output": "test/output/date_format_output.csv",
                      "config": "test/config/date_format_config.txt"}],
                      "Merge Column": [
                      {"name": "Merge Columns first_name and last_name",
                      "input": "test/input/merge_column_input.csv", 
                      "output": "test/output/merge_column_output.csv",
                      "config": "test/config/mergecolumn_config.txt"}],
                      "Filter Column": [
                      {"name": "Remove items which has the age greater than 50",
                      "input": "test/input/filtering_input.csv", 
                      "output": "test/output/filtering_output.csv",
                      "config": "test/config/filtering_config.txt"}],
                      "Create New Column": [
                      {"name": "create a new column eligible_for_voting with the value as T if age > 18 else F",
                      "input": "test/input/new_col_input.csv", 
                      "output": "test/output/new_col_output.csv",
                      "config": "test/config/new_column_config.txt"}
                      ]
                    }
    return testcase_dict

def run_test():
    print("****************** Running testcases ******************\n")
    all_testcases = get_testcases()
    for testcases in all_testcases:
        print("Running testcases for : %s" %testcases)
        for i, testcase in enumerate(all_testcases[testcases]):
            print("Testcase No. %s : %s" % (i+1, testcase['name']))
            csv_manager = CSVManager(testcase['input'], 
                                     testcase['output'],
                                     testcase['config'])
            print(csv_manager.generate_csv_based_on_configuration())
        print("Testcases for : %s Completed." %testcases)

def validate_arguments(arguments):
    if len(arguments) < 4:
        raise RuntimeError("Please make sure that you are provided all the arguments.")    
    data = {"input": arguments[1], 
            "output": arguments[2],
            "config": arguments[3]}

    for field, value in data.items():
        if field != "output":        
            if not path.isfile(value) or not path.exists(value):
                raise RuntimeError("Please provide valid path for %s: %s" % (field, value))
    return data

def read_help():
    with open('readme.md', 'r') as help_file:
        lines = help_file.readlines()
        for line in lines:
            print(line)   


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) == 1:
        raise RuntimeError("Please provide valid arguments. try --help for more details")
    elif arguments[1] == "--test":
        run_test()
    elif arguments[1] == "--help":
        read_help()
    else:
        cleaned_args = validate_arguments(arguments)
        csv_manager = CSVManager(cleaned_args['input'], 
                                 cleaned_args['output'],
                                 cleaned_args['config'])
        print(csv_manager.generate_csv_based_on_configuration())


