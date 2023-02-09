#!/usr/bin/python3 

### ABOUT SCRIPT ###
# This script takes a log file and uses regex to parse through it.
# It produces two different csv files: One that lists the errors and the number of occurances
# Two: Provides a csv by user and the total number of INFO and ERROR messages they have generated.


import re
import operator
import csv


#Create needed variables to use later.
error_dict = {}
user_count = {}

#Create regex for matching ERROR and INFO
error_regex = r"ERROR [\w' ]*"
full_error_regex = r"ERROR [\w' \[#\]]* \([\w.\w]*\)"

info_regex = r"INFO [\w' ]*"
full_info_regex = r"INFO [\w' \[#\]]* \([\w.\w]*\)"

username_regex = r"\([\w.\w]*\)"

#Open log file and use the regexs to find matches
#Just looking for ERROR and INFO
#Creates a raw dictionary that we will use to then make new CSV files later. The dictionary just makes and entry for users and the number of INFO and ERRORS for each.
with open("./syslog.log", "r") as log:
    log_list = log.readlines()
    for entry in log_list:
        error_match = re.search(error_regex, entry)
        full_error_match = re.search(full_error_regex, entry)
        full_info_match = re.search(full_info_regex, entry)
        if full_error_match != None:
            error_text = full_error_match.group(0)
            username = re.search(username_regex, error_text).group(0).strip("()")
            #This portion below will take the User and add them if they are not in the list and increment the error count.
            if username not in user_count.keys():
                user_count[username] = {"ERROR": 1, "INFO": 0}
            else:
                user_count[username]["ERROR"] = user_count[username]["ERROR"] + 1
        if full_info_match != None:
            info_text = full_info_match.group(0)
            username = re.search(username_regex, info_text).group(0).strip("()")
            #This portion will take the User and add them if they are not in the list and increment the info count.
            if username not in user_count.keys():
                user_count[username] = {"ERROR": 0, "INFO": 1}
            else:
                user_count[username]["INFO"] = user_count[username]["INFO"] + 1
    sorted_user_list = sorted(user_count.items(), key = operator.itemgetter(0))

# Looks for error messages and adds them to the error dictionary
with open("./syslog.log", "r") as log:
    log_list = log.readlines()
    for entry in log_list:
        error_match = re.search(error_regex, entry)
        full_error_match = re.search(full_error_regex, entry)
        full_info_match = re.search(full_info_regex, entry)
        username = ""
        if error_match != None:
            error_text = error_match.group(0)
            error_msg = (error_text.strip("ERROR ")).strip(" ")
        # Now check to see if error message is in the error_dict dictionary.
            if error_msg not in error_dict.keys():
                error_dict[error_msg] = 1
            else:
                error_dict[error_msg] = error_dict[error_msg] + 1
        sorted_errors = sorted(error_dict.items(), key = operator.itemgetter(1), reverse=True)                

#print(user_count)
#print(user_count["ac"]["ERROR"])
# 
#sorted_user_list = sorted(user_count.items(), key = operator.itemgetter(0))
#print(sorted_user_list)
#print(error_dict)
#print(sorted_errors)
                
#sorted_errors.insert(0, ("Error", "Count"))
#print(sorted_errors)

# Takes the sorted dictionaries that are now lists with tuples in them and createds new csv files.
with open("/home/netrunner/Documents/Google_IT_Automation/Projects/errors_message.csv", "w") as file: # You will need to use your specific path
    index = 0
    fieldnames = ["Error", "Count"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for error in sorted_errors:
        #Creates a new CSV file that takes each error message that occurs in the syslog file and then adds the number of times it occurs. 
        writer.writerow({"Error": sorted_errors[index][0], "Count": sorted_errors[index][1]})
        index = index + 1

with open("/home/netrunner/Documents/Google_IT_Automation/Projects/user_statistics.csv", "w") as file:
    index = 0
    fieldnames = ["Username", "INFO", "ERROR"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for stats in sorted_user_list:
        #Creates the new CSV file with each user and the number of INFO and ERROR messages they generated. 
        writer.writerow({"Username": sorted_user_list[index][0], "INFO": sorted_user_list[index][1]["INFO"], "ERROR": sorted_user_list[index][1]["ERROR"]})
        index = index + 1

