import os
import json
INST_USER= INST_PASS= DATABASE_PATH= CHROME_DRIVER_PATH= ''
RUN_MODE = LIKES_LIMIT= DAYS_TO_UNFOLLOW= CHECK_FOLLOWERS_EVERY= RUN_DURATION = 0
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
    RUN_MODE = obj['config']['run_mode']
    LIKES_LIMIT = obj['config']['likes_over']
    CHECK_FOLLOWERS_EVERY= obj['config']['check_followers_every']
    RUN_DURATION = obj['config']['run_dauration']
    HASHTAGS = obj['config']['hashtags']
    DAYS_TO_UNFOLLOW = obj['config']['days_to_unfollow']


def update_settings_file():
    json_data = {
      "paths": {
        "db_path": DATABASE_PATH,
        "chrome_driver_path": CHROME_DRIVER_PATH
      },
      "instagram": {
        "user": INST_USER,
        "pass": INST_PASS
      },
      "config": {
        "run_mode": RUN_MODE,
        "days_to_unfollow": DAYS_TO_UNFOLLOW,
        "likes_over": LIKES_LIMIT,
        "check_followers_every": CHECK_FOLLOWERS_EVERY,
        "run_dauration": RUN_DURATION,
        "hashtags": HASHTAGS
      }
    }
    with open(os.getcwd()+'/settings.json', 'w+') as json_file:
        json.dump(json_data, json_file, indent = 1, separators=(',', ':'))
