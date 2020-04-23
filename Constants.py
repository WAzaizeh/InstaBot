import os
import json
INST_USER= INST_PASS= DATABASE_PATH= DATABASE_NAME= CHROME_DRIVER_PATH= ''
LIKES_LIMIT= DAYS_TO_UNFOLLOW= CHECK_FOLLOWERS_EVERY= 0
HASHTAGS = []

def init():
    global INST_USER, INST_PASS, DATABASE_PATH,DATABASE_NAME,CHROME_DRIVER_PATH,\
        LIKES_LIMIT, DAYS_TO_UNFOLLOW, CHECK_FOLLOWERS_EVERY, HASHTAGS
    # read file
    data = None
    with open(os.getcwd()+'/settings.json', 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)
    INST_USER = obj['instagram']['user']
    INST_PASS = obj['instagram']['pass']
    DATABASE_PATH = obj['paths']['filepath']
    DATABASE_NAME = obj['paths']['name']
    CHROME_DRIVER_PATH = obj['paths']['chrome_driver_path']
    LIKES_LIMIT = obj['config']['likes_over']
    CHECK_FOLLOWERS_EVERY=obj['config']['check_followers_every']
    HASHTAGS = obj['config']['hashtags']
    DAYS_TO_UNFOLLOW = obj['config']['days_to_unfollow']
