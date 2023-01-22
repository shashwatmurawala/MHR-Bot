import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

from tkinter import *

resources_lst = "Resources List:\n"

def show_list():
    list_window = Toplevel(root)
    list_window.title("List")

    my_list = ["item 1", "item 2", "item 3"]
    list_label = Label(list_window, text=my_list)
    list_label.pack()

    close_button = Button(list_window, text="Close", command=list_window.destroy)
    close_button.pack()

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *

questions_lst = ["Are you experiencing feelings of depression or sadness?[y/n]",
                 "Have you been struggling with anxiety or stress?[y/n]",
                 "Are you having trouble sleeping or experiencing insomnia?[y/n]",
                 "Do you have difficulty concentrating or focusing on tasks?[y/n]",
                 "Are you experiencing feelings of hopelessness or helplessness?[y/n]",
                 "Are you having trouble with relationships or social interactions?[y/n]",
                 "Are you experiencing symptoms of a traumatic event?[y/n]",
                 "Are you experiencing any symptoms of an eating disorder?[y/n]",
                 "Are you experiencing any symptoms of a substance use disorder?[y/n]",
                 "Have you ever considered harming yourself or others?[y/n]",
                 "What university do you attend?Type the corresponding letter\n(a)University of Toronto\n(b)University of Waterloo\n(c)Queens University\n(d)McMaster University\n(e)Wilfrid Laurier University\n(f)University of Guelph\n(g)Other",
                 "Would you like to be given preferences based on your postal code? If yes please type the first 3 characters of your postal code. If no then type n."]

user_responses =[]
question_index = 0

def q1():
    global resources_lst
    print(user_responses)
    if user_responses[1] == "y":
        resources_lst += "• https://www.canada.ca/en/public-health/services/chronic-diseases/mental-illness/what-help-myself-feel-depressed.html\n"

    else:
        resources_lst += ""

    if user_responses[2] == "y":
        resources_lst += "• https://www.canada.ca/en/health-canada/services/healthy-living/your-health/diseases/mental-health-anxiety-disorders.html\n"
        

    else:
        resources_lst += ""

    if user_responses[3] == "y":
        resources_lst += "• https://www.insomnia-help.net/\n"

    else:
        resources_lst += ""
    
    if user_responses[4] == "y":
        resources_lst += "• https://caddac.ca/\n"

    else:
        resources_lst += ""
        
    if user_responses[5] == "y":
        resources_lst += "• https://www.cbc.ca/news/canada/british-columbia/feeling-helpless-in-the-wake-of-covid-19-here-are-6-things-you-can-do-1.5507376\n"
    

    else:
        resources_lst += ""
        
    if user_responses[6] == "y":
        resources_lst += "• https://findahelpline.com/ca/on/topics/relationships\n"
        

    else:
        resources_lst += ""
    
    if user_responses[7] == "y":
        resources_lst += "• https://www.canada.ca/en/public-health/topics/mental-health-wellness/post-traumatic-stress-disorder.html\n"
        

    else:
        resources_lst += ""
        
    if user_responses[8] == "y":
        resources_lst += "• https://edfc.ca/resources-2/\n"
    

    else:
        resources_lst += ""
        

    if user_responses[9] == "y":
        resources_lst += "• https://www.canada.ca/en/health-canada/services/substance-use/get-help-problematic-substance-use.html\n"
        

    else:
        resources_lst += ""

    if user_responses[10] == "y":
        resources_lst += "• https://talksuicide.ca/\n"

    else:
        resources_lst += ""

    if user_responses[11] == "a":
        resources_lst += "• https://studentlife.utoronto.ca/service/mental-health-clinical-services/\n"

    elif user_responses[11] == "b":
        resources_lst += "• https://uwaterloo.ca/campus-wellness/get-mental-health-support-when-you-need-it\n"

    elif user_responses[11] == "c":
        resources_lst += "• https://www.queensu.ca/studentwellness/mental-health\n"
        

    elif user_responses[11] == "d":
        resources_lst += "• https://wellness.mcmaster.ca/thriveweek/mentalhealthresources/\n"
    

    elif user_responses[11] == "e":
        resources_lst += "• https://students.wlu.ca/wellness-and-recreation/health-and-wellness/services/mental-health.html\n"
        

    elif user_responses[11] == "f":
        resources_lst += "• https://wellness.uoguelph.ca/services/counselling/mental-health-support-resources\n"
        

    else:
        resources_lst += "hi"

    if user_responses[12] == "M5R":
        resources_lst += "• https://www.pathway-therapy.com/\n"

    elif user_responses[12] == "M5S":
        resources_lst += "• https://www.firstsession.com/\n"

    elif user_responses[12] == "M5T":
        resources_lst += "• http://www.camh.ca/\n"

    elif user_responses[12] == "M5N":
        resources_lst += "• https://www.elisplace.org/\n"
                                                            
    elif user_responses[12] == "N2L":
        resources_lst += "• https://www.grhosp.on.ca/\n"

    elif user_responses[12] == "N2T":
        resources_lst += "• https://lindsayspeirs.ca/\n"

    elif user_responses[12] == "N2M":
        resources_lst += "• https://heartnmind.ca/\n"

    elif user_responses[12] == "N2J":
        resources_lst += "• https://www.grhosp.on.ca/\n"

    elif user_responses[12] == "K7L":
        resources_lst += "• https://amhs-kfla.ca/\n"

    elif user_responses[12] == "K7K":
        resources_lst += "• https://www.thelighthouse-lephare.ca/\n"

    elif user_responses[12] == "L8S":
        resources_lst += "• https://www.advancehealth.ca/psychotherapy-landing\n"

    elif user_responses[12] == "L8P":
        resources_lst += "• https://cmhahamilton.ca/\n"

    elif user_responses[12] == "N1E":
        resources_lst += "• https://homewoodhealth.com/health-centre\n"

    elif user_responses[12] == "N1G":
        resources_lst += "• https://cmhaww.ca/\n"

    elif user_responses[12] == "N1L":
        resources_lst += "• https://www.kstherapyservices.ca/\n"

    elif user_responses[12] == "N1H":
        resources_lst += "• https://www.counsellingguelph.com/\n"

    else:
        resources_lst += ""

    return resources_lst
        

def send():
    global question_index
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if msg != '':
        CurrentChat.config(state=NORMAL)
        CurrentChat.insert(END, "You: " + msg + '\n\n')
        CurrentChat.config(foreground="#442265", font=("Verdana", 12 ))
    
        user_responses.append(msg)
        if question_index < len(questions_lst):
            CurrentChat.insert(END, "MHR Finder Bot: " + questions_lst[question_index] + '\n\n')
            question_index += 1

        else:
            output = q1()
            CurrentChat.insert(END, "" + output)
            question_index += 1
            
    CurrentChat.config(state=DISABLED)
    CurrentChat.yview(END)

def display_message():
    CurrentChat.config(state=NORMAL)
    CurrentChat.insert(END, "Hello, my name is the Mental Health \nResources Finder Bot, but you can call me \nMHR for short. \n\nRespond to start" + '\n\n')
    CurrentChat.config(foreground="#442265", font=("Verdana", 12 ))
    CurrentChat.config(state=DISABLED)
    CurrentChat.yview(END)
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
        CurrentChat.config(state=NORMAL)
        CurrentChat.insert(END, "You: " + msg + '\n\n')
        CurrentChat.config(state=DISABLED)
        CurrentChat.yview(END)
        
        
 

base = Tk()
base.title("MHR Finder Bot")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg = "SkyBlue2")

#The following creates a new Chat window
CurrentChat = Text(base, bd=0, bg="SkyBlue2", height="8", width="50", font="Arial",)

CurrentChat.config(state=DISABLED)

initial_response = chatbot_response("Hello")
CurrentChat.insert(END, "MHR Finder Bot: " + initial_response + '\n\n')


#This creates a bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=CurrentChat.yview, cursor="heart")
CurrentChat['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send    ", width="12", height=5,
                    bd=0, bg="#23b076", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

#Place all components on the screen
scrollbar.place(x=377,y=7, height=387)
CurrentChat.place(x=7,y=7, height=387, width=371)
EntryBox.place(x=129, y=402, height=91, width=266)
SendButton.place(x=7, y=402, height=91)

display_message()
base.mainloop()
