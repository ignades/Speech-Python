import speech_recognition as sr
from write_doc import *
from inquirer_form_loop import *
r = sr.Recognizer()


def record_text():
    #loop in case of error
    while(1):
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                #Prepare

                r.adjust_for_ambient_noise(source2, duration=0.2)

                #listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                MyText = r.recognize_google(audio2,language="it-IT")



                #return MyText = MyText.lower()
                print(MyText)
                #os.system(MyText)
                return MyText


        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
    return

testo = record_text()

if testo=="scrivi":
        doc_to_edit = create_inquirer()
        doc_edit = doc_to_edit.replace("./", "")
        print(doc_edit)
        testo = record_text()
        write_documento(doc_edit,testo)
