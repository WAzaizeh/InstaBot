
from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


questions = [
    {
        'type': 'list',
        'message': 'New or first time user?',
        'name': 'reconfigure',
        'choices': [{'name': 'Yes'}, {'name': 'No'} ]
    },
    {
        'type': 'input',
        'name' : 'username',
        'message': 'Enter username:',
        'when': lambda answers: answers['reconfigure'] == 'Yes'
    },
    {
        'type': 'password',
        'name': 'password',
        'message' : 'Enter password:',
        'when': lambda answers: answers['reconfigure'] == 'Yes'
    },
    {
        'type': 'input',
        'name' : 'chrome_driver_path',
        'message': 'Path to chrome webdriver:',
        # need filepath autocomplete and validator
        'when': lambda answers: answers['reconfigure'] == 'Yes'
    }
]

answers = prompt(questions, style=style)
pprint(answers)
