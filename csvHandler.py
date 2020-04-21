import os.path
import csv
import Constants
import fileinput
import sys
import TimeHelper

class csvHandler(object):
    Constants.init()
    DATABASE_PATH = Constants.DATABASE_PATH
    DATABASE_NAME = Constants.DATABASE_NAME

    def __init__(self):
        if csvHandler.DATABASE_PATH == '': # if no path is specified, save in the same file
            csvHandler.DATABASE_PATH = os.getcwd() + '/' + Constants.DATABASE_NAME + '.csv'
            try:
                if not os.path.isfile(csvHandler.DATABASE_PATH):
                    headers = ['Username', 'Date']
                    with open(csvHandler.DATABASE_PATH, 'a+') as f:
                        writer = csv.writer(f)
                        writer.writerow(headers)
            except OSError: # to handle error when file exists and cannot be accessed
                pass


    # add new user
    def add_user(username, current_date):
        with open(csvHandler.DATABASE_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([username, current_date])

    # delete user by username
    def delete_user(username):
        with open(csvHandler.DATABASE_PATH, "r") as f:
            data = list(csv.reader(f))

        with open(csvHandler.DATABASE_PATH, "w") as f:
            writer = csv.writer(f)
            for row in data:
                if row[0] != username:
                    writer.writerow(row)

    # check if any user qualifies to be unfollowed
    def check_unfollow_list(self):
        with open(self.DATABASE_PATH, "r") as f:
            data = list(csv.reader(f))
        users_to_unfollow = []
        for row in data[1:]: # skip headers
            d = TimeHelper.days_since_date(row[1])
            if d >= Constants.DAYS_TO_UNFOLLOW:
                users_to_unfollow.append(row[0])
        return users_to_unfollow

    # get all followed users
    def get_followed_users(self):
        users = []
        with open(self.DATABASE_PATH, "r") as f:
            data = list(csv.reader(f))
        for row in data[1:]:
            users.append(row[0])
        return users
