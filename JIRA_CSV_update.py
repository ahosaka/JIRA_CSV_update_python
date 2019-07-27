# /usr / bin / python2.7
# python 2.7
# a python script for analysts
# no pandas used
# csv files should be always the same format!!
# add comment
# add label

# how to use
# dependency: jira module
# 0. If you don't have jira, then pip install jira or pip install -r requirements.txt in the directory where the script locates

# 1. Open termanal and navigated to the directory where this script locates
# 2. type "python JIRA_CSV_update.py" in terminal
# 3. You will be asked to type in or drag&drop CSV file into the termanal window
# 4. Then hit the Enter
# 5. A logging file will be generated automatically

import csv
import logging
from jira import JIRA
from jira.client import JIRA

logging_message = ''
logging.basicConfig(filename="JIRA_CSV_updated.log",
                    level=logging.INFO, format='%(asctime)s: \n%(message)s')

# jira login
options = {'server': 'your Jira URL'}
usr = 'username'
pas = 'password'

jira = JIRA(options=options, basic_auth=(usr, pas))
# print("Login!!")

csv_input = raw_input(
    '>> Type your CSV file name or Drag and drop the CSV file here: ')
csv_input = csv_input.split('/')[-1].strip()
print('>> Working on ' + csv_input)

# add comment and label


def update_JIRA(your_issue_key, your_keyword):
    ticket = jira.issue(your_issue_key)
    message = "your keyword is {0}".format(
        your_keyword)
    jira.add_comment((your_issue_key), message)
    ticket.fields.labels.append('your_tag')
    ticket.update(fields={"labels": ticket.fields.labels})
    update_message = '{0}: {1}\n'.format(your_issue_key, your_keyword)

    return update_message


def execute_JIRA(tickets_list, logging_message):
    for i in tickets_list:
        print(i[0] + ': ' + i[1])
        update_message = update_JIRA(i[0], i[1])

        logging_message += update_message

    logging.info(logging_message)

    return


def catch_error(logging_message):

    try:
        # open csv file with encoding="utf-8"
        with open(csv_input) as f:
            reader = csv.reader(f)
            csv_list = [[row[0], row[4]] for row in reader if row[4] != '']

        Jire_ticket_list = csv_list[1:]
        len_keywords = len(Jire_ticket_list)
        if len_keywords != 1:
            logging_message += (
                'The following {0} JIRA tickets have been updated!\nJIRA Tickets: your_keyword\n'.format(len_keywords))
            print 'The following {0} JIRA tickets will be updated!'.format(len_keywords)
        else:
            logging_message += (
                'The following {0} JIRA ticket has been updated!\nJIRA Tickets: your_keyword\n'.format(len_keywords))
            print 'The following {0} JIRA ticket will be updated!'.format(len_keywords)

        execute_JIRA(Jire_ticket_list, logging_message)
        print ">> Update Completed!"

    except Exception as e:
        print "Update Failed. Make sure that your CSV file exists in this directory."
        raise e
    return


if __name__ == '__main__':
    catch_error(logging_message)
