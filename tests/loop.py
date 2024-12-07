import inquirer
import array
import glob


def create_inquirer():
    docs =  glob.glob('./*.docx')
    l = len(docs)
    #return print(l)
    all_choices = []

    if(l == 0):
        message= "Crea un nuovo Documento!"
        print(message)
        return  message
    else:

        for idx, x in enumerate(docs):
            all_choices.insert(idx, x)

        questions = [
          inquirer.List('size',
                        message="Choice a document to edit?",
                        choices=all_choices,
                    ),
        ]

        answers = inquirer.prompt(questions)
        print(answers['size'])
        return  answers['size']


create_inquirer()
