import re
import inquirer
from pprint import pprint



def give_name():
    questions = [
      inquirer.Text('doc_name', message="scegli un nome per il documento:"),
     # inquirer.Text('surname', message="What's your surname"),
      #inquirer.Text('phone', message="What's your phone number",
        #            validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),
            #        )
    ]
    answers =  inquirer.prompt(questions)
    #print(answers['doc_name'])
    return answers['doc_name']

#question()
