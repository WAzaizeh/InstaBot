import os
import json
INST_USER= INST_PASS= DATABASE_PATH= DATABASE_NAME= CHROME_DRIVER_PATH= ''
LIKES_LIMIT= DAYS_TO_UNFOLLOW= CHECK_FOLLOWERS_EVERY= RUN_DURATION = 0
HASHTAGS = []

def init():
    global INST_USER, INST_PASS, DATABASE_PATH,DATABASE_NAME,CHROME_DRIVER_PATH,\
        LIKES_LIMIT, DAYS_TO_UNFOLLOW, CHECK_FOLLOWERS_EVERY, HASHTAGS
    # read file
    data = None
    with open(os.getcwd()+'/settings.json', 'r') as json_file:
        data = json_file.read()
    obj = json.loads(data)
    INST_USER = obj['instagram']['user']
    INST_PASS = obj['instagram']['pass']
    DATABASE_PATH = obj['paths']['db_path']
    CHROME_DRIVER_PATH = obj['paths']['chrome_driver_path']
    LIKES_LIMIT = obj['config']['likes_over']
    CHECK_FOLLOWERS_EVERY= obj['config']['check_followers_every']
    RUN_DURATION = obj['config']['run_dauration']
    HASHTAGS = obj['config']['hashtags']
    DAYS_TO_UNFOLLOW = obj['config']['days_to_unfollow']


def update_settings_file():
    data = []
    with open('/settings.json', 'r') as json_file:
        json.dump(data, json_file)
    print(INST_USER, INST_PASS)
    # triggered by CLI to modify some variable based on name of what's send?
