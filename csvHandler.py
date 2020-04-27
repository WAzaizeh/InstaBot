import os, os.path
import csv
import Constants, TimeHelper
import pandas as pd
import datetime as dt

class csvHandler(object):
    Constants.init()

    def __init__(self):
        if Constants.DATABASE_PATH == '': # if no path is specified, save in the same file
            Constants.DATABASE_PATH = os.getcwd() + '/' + Constants.INST_USER + '.csv'
        try:
            if not os.path.isfile(Constants.DATABASE_PATH):
                headers = ['username', 'date']
                with open(Constants.DATABASE_PATH, 'a+') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                Constants.update_settings_file() # save into the settings file
        except OSError: # to handle error when file exists and cannot be accessed
            pass

    # add new user
    def add_user(username):
        current_df = pd.read_csv(Constants.DATABASE_PATH, index_col=False)
        date = dt.datetime.now().date()
        current_df = current_df.append({'username': username, 'date' : date}, ignore_index=True)
        current_df.to_csv(Constants.DATABASE_PATH, index=False)

    # delete user by username
    def delete_user(username):
        current_df = pd.read_csv(Constants.DATABASE_PATH, index_col=False)
        current_df = current_df[current_df.username != username]
        current_df.to_csv(Constants.DATABASE_PATH, index=False)

    # check if any user qualifies to be unfollowed
    def check_unfollow_list(self):
        current_df = pd.read_csv(Constants.DATABASE_PATH, index_col=False)
        users_to_unfollow = []
        for _, row in current_df.iterrows():
            d = TimeHelper.days_since_date(row['date'])
            if d >= Constants.DAYS_TO_UNFOLLOW:
                users_to_unfollow.append(row.username)
        return users_to_unfollow

    # get all followed users
    def get_followed_users(self):
        current_df = pd.read_csv(Constants.DATABASE_PATH, index_col=False)
        users=[]
        if current_df.shape[0] > 0:
            users = list(current_df['username'])
        return users
