# -*- coding: utf-8 -*-
"""
hierarchical prompt usage example
"""
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError
import os


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


class HashtagListValidator(Validator):
    def validate(self, value):
        hashtag_list = (value.text).replace(' ', '')
        by_comma_num = len(hashtag_list.split(','))
        by_whitespace_num = len(value.text.split())
        if len(hashtag_list):
            if '#' not in hashtag_list:
                if by_comma_num == by_whitespace_num:
                    return True
                else:
                    raise ValidationError(
                        message="Use commas to seperate hashtags",
                        cursor_position=len(value.text))
            else:
                raise ValidationError(
                    message="Don't include #",
                    cursor_position=len(value.text))
        else:
            print('Please enter a list of hashtags')


def main():
    print('Welcome to InstaBot')
    settup_account()


def settup_account():
    new_user_q = {
        'type': 'list',
        'name': 'new_user',
        'message': 'Are you a new user?',
        'choices': ['Yes', 'No']
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
    else:
        print('You cannot go that way')


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
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'likes_max',
        'message': 'Max number of likes per post to follow and like:',
        'validate': NumberValidator

    },
    {
        'type': 'input',
        'name': 'check_followers_every',
        'message': 'Follow & like every (minutes):',
        'validate': NumberValidator
    },
    {
        'type': 'input',
        'name': 'hashtags_list',
        'message': 'List of hashtags seperated by commas(,) and without the (#):',
        'validate': HashtagListValidator
    }]
    prompt(settings_q)



if __name__ == '__main__':
    main()
