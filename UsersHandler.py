from csvHandler import *
import datetime

#delete user by username
def delete_user(username):
    csvHandler.delete_user(username)


#add new username
def add_user(username):
    now = datetime.datetime.now().date()
    csvHandler.add_user(username, now)


#check if any user qualifies to be unfollowed
def check_unfollow_list():
    db = csvHandler()
    users_to_unfollow = db.check_unfollow_list()
    return users_to_unfollow


#get all followed users
def get_followed_users():
    db = csvHandler()
    users = db.get_followed_users()
    return users
