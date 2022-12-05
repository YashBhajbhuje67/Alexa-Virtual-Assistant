from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from email import message
from posixpath import commonpath
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
from datetime import date
import wikipedia
import pyjokes
import webbrowser
from wikipedia.wikipedia import search
import requests
import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


talk('Hello! My name is Alexa. How can I help you?')


def summarize(text):
    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Creating a frequency table to keep the
    # score of each word

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score
    # of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence
    print(summary)
    talk(summary)


def pos(sentence):
    wiki = ' '
    tokens = word_tokenize(sentence)
    print(nltk.pos_tag(tokens))
    for j, i in nltk.pos_tag(tokens):
        if(i == 'NN' or i == 'NNP' or i == 'NNS' or i == 'NNPS'):
            wiki = wiki + " " + j
    return wiki

# voice to text function
def take_command():
    command = ''
    try:
        # source = speech_recognition.Microphone()
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source, phrase_time_limit=4)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')

    except:
        pass
    return command

# main function
def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song + 'in your browser')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print('Current time is ' + time)
        talk('Current time is ' + time)

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(pos(person))
        summarize(info)

    elif 'what is' in command:
        thing = command.replace('what is', '')
        inf = wikipedia.summary(pos(thing))
        summarize(inf)

    elif 'location' in command:
        location = command.replace('give me the location for', ' ')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        talk('Here is the location for' + location)

    elif 'search for' in command:
        search = command.replace('search for', ' ')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        talk('here is what i found for' + search)

    elif "tell me today's date" in command:
        today = date.today()
        print("today's date is", today)
        talk(today)

    elif 'message' in command:
        talk('Whom do you want to send the message')
        # 9307870496
        to = take_command()
        rec = '+91'+ to
        print(rec)
        talk('what message do you wanna send?')
        mes = take_command()
        pywhatkit.sendwhatmsg_instantly(rec, mes,  20)

    elif 'weather' in command:
        talk('Please tell the name of the city')
        city = take_command()
        url = 'https://wttr.in/{}'.format(city)
        res = requests.get(url)
        print(res.text)

    elif 'joke' in command:
        fun = pyjokes.get_joke()
        print(fun)
        talk(fun)
    elif 'exit' in command:
        talk('byebye take care')
        exit()
    else:
        talk('Please say the command again.')

# i=1
# while(i<=2):
#     run_alexa()
#     i=i+1


while(True):
    run_alexa()
