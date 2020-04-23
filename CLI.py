# -*- coding: utf-8 -*-
"""
A personal customized InstaBot
"""
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError
import os
import string


class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="Please enter a proper file path",
                cursor_position=len(value.text))


class NumberValidator(Validator):
    def validate(self, value):
        try:
            int(value.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(value.text))


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="Please enter a vlaue",
                cursor_position=len(value.text))


class HashtagValidator(Validator):
    def validate(self, value):
        special_character = string.punctuation.replace('_',' ') # underscore is valid but whitespace is not
        if len(value.text):
            if any(char in special_character for char in value.text):
                raise ValidationError(
                    message="Only letters, numbers, and underscore (_) are valid",
                    cursor_position=len(value.text))
            else:
                return True
        else:
            raise ValidationError(
                message="Enter a valid hashtag name",
                cursor_position=len(value.text))


def main():
    print('Welcome to InstaBot')
    settup_account()


def settup_account():
    new_user_q = {
        'type': 'list',
        'name': 'new_user',
        'message': 'Are you a new user?',
        'choices': ['Yes', 'No'],
        'default': 2
    }
    answer = prompt(new_user_q)
    print(answer['new_user'])
    if (answer['new_user'] == 'Yes'):
        get_username_pass()
        get_chrome_driver_path()
        change_settings()
    else:
        change_settings()


def get_username_pass():
    user_q = {
        'type': 'input',
        'name': 'username',
        'message': 'Enter your Instagram account username:',
        'validate': EmptyValidator
    }
    username = prompt(user_q)
    password_q = {
        'type': 'password',
        'name': 'password',
        'message': 'Enter your Instagram account password:',
        'validate': EmptyValidator
    }
    password = prompt(password_q)


def get_chrome_driver_path():
    chromedriver_path_q = {
        'type': 'input',
        'name': 'exe_path',
        'message': 'Enter the full path to your Chrome Driver:',
        'validate': FilePathValidator
    }
    chromedriver_path = prompt(chromedriver_path_q)


def change_settings():
    change_q = {
        'type': 'list',
        'name': 'change_settings',
        'message': 'Would you like to change the default settings?',
        'choices': ['Yes', 'No']
    }
    answer = prompt(change_q)
    if answer['change_settings'] == 'Yes':
        get_settings()


def get_settings():
    settings_q = [{
        'type': 'list',
        'name': 'follow_status',
        'message': 'Which functions would you like to run?',
        'choices': ['Follow & Unfollow', 'Follow only', 'Unfollow only']
    },
    {
        'type': 'input',
        'name': 'days_to_unfollow',
        'message': 'Days to unfollow:',
        'default': '3',
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'likes_max',
        'message': 'Max number of likes per post to follow and like:',
        'default': '150',
        'validate': NumberValidator

    },
    {
        'type': 'input',
        'name': 'check_followers_every',
        'message': 'Follow & like every (minutes):',
        'default': '10',
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'run_for',
        'message': 'Run for (minutes):',
        'default': '60',
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'hashtag_num',
        'message': 'How many hashtags would you like to follow & like?',
        'default': '4',
        'validate': NumberValidator
    }]
    answers = prompt(settings_q)
    hashtag_list = []
    for i in range(int(answers['hashtag_num'])):
        new_hashtag = generate_hashtag_list()
        hashtag_list.append(new_hashtag)
    print(hashtag_list)


def generate_hashtag_list():
    hashtag_list_q = {
        'type': 'input',
        'name': 'hashtags',
        'message': 'Enter hashtag without the (#):',
        'validate': HashtagValidator
    }
    hashtag = prompt(hashtag_list_q)
    return hashtag['hashtags']


if __name__ == '__main__':
    main()
