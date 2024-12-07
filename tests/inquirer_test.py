import re
import inquirer
from pprint import pprint




def question():string()
questions = [
  inquirer.Text('name', message="scegli carattere speciale:"),
 # inquirer.Text('surname', message="What's your surname"),
  #inquirer.Text('phone', message="What's your phone number",
    #            validate=lambda _, x: re.match('\+?\d[\d ]+\d', x),
        #        )
]



answers = inquirer.prompt(questions)

print("Scrivendo..Special caratter")
f=open("output_text.txt","a")
f.write(answers["name"])
#f.write("\n")
f.close()
