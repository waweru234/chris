import speech_recognition as sr
import pyttsx3
import subprocess
import random
import pygetwindow as gw
import webbrowser
import requests
import pyautogui
import threading
import time
from PIL import ImageGrab
import os
import ctypes
import pyperclip       
import google.generativeai as genai
import azure.cognitiveservices.speech as speechsdk
from pathlib import Path
from openai import OpenAI
import comtypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
token = "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"
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
client = client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
global respons 
global y
global outfit
global random_movie
global movie_files
global search_keyword
global found_file
chrome_process = None
root_directory = "D:\\"  # You can specify the root directory for the search (e.g., "/" for Unix-like systems)
search_keyword = "grown"
# Global variable to store the Chrome process
def removebackground():
    response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('kenyatta university logo.jpg', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'MHLSNS7DDq8aY4jdBfsQcWgd'},
    )
    if response.status_code == requests.codes.ok:
     with open('no-bg.png', 'wb') as out:
        out.write(response.content)
    else:
      print("Error:", response.status_code, response.text)

def wait():
    ac =True                                                                                                                                      
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        while ac:
         audio = recognizer.listen(source, timeout=3600, phrase_time_limit=7)
         try:
            print("Recognizing...")
            user_inpu = recognizer.recognize_google(audio).lower()
            user_inpu=symbols(user_inpu)
            print(user_inpu) 
            if"restart" in user_inpu:
                re=random.choice(["Restarting your computer! I will miss you boss",
                                "Goodbye boss! till next time"
                                "Talk to you later boss! goodbye"]) 
                speak_text(re)   
                restart_computer()
                ac= False
            elif"sleep mode" in user_inpu:
                re=random.choice(["Putting your computer to sleep! I will miss you boss",
                                "Goodbye boss! till next time"
                                "Talk to you later boss! goodbye",
                                "your computer will be put to sleep mode"]) 
                speak_text(re)
                sleep_computer()
                ac=False
            elif "sleep" in user_inpu or"bye" in user_inpu:
                print("You said:", user_inpu)   
                re =random.choice(["Going to sleep, boss! Till next time.",
                                "Farewell! See you later.",
                                  "Goodbye! Have a great day!",
                                  "i will miss you boss! You can call on me in case of anything","i have gone to sleep you will have to wake me manually after this"]) 
                speak_text(re)
                ac = False 
            elif"power" in user_inpu or "off" in user_inpu or "turn" in user_inpu:
                res=random.choice(["Turning off your computer! I will miss you boss",
                                "Goodbye boss! till next time"
                                "Talk to you later boss! goodbye",
                                "shutting down your computer sir",
                                "your computer will be turned off"])
                speak_text(res)
                power_off_computer()
                ac=False
            elif "wake" in user_inpu or"chris" in user_inpu or "hello" in user_inpu or "jim" in user_inpu or "gym" in user_inpu :
                print("You said:", user_inpu)   
                re = random.choice([
                                 "I am here, boss.",
                                 "Hello! I am here! How can I help you?", 
                                 "Hi there! What can I do for you?",
                                 "Hello! my creator! I am awake! and I have missed you.",
                                 "i have missed you bro! how can i be of assistance",
                                 "Hello! I am here! How can I help you?", 
                                 "Hi there! What can I do for you?",
                                 "Hello! my creator! I am awake! and I have missed you.",
                                 "heeey, thank you for calling on me, what do you want me to do now?",
                                 "I have been waiting for you to call on me. What do you want me to do now?",
                                 "i have been waiting for your call"
                                 ])
                speak_text(re)
                litsen_and_respond()
         except sr.UnknownValueError:
              print("nothing found")     
         except sr.RequestError as e:
         
              print(f"Could not request results from Google Speech Recognition service; {e}") 
def copy_to_clipboard():
    # Simulate pressing the Ctrl key and holding it down
    pyautogui.keyDown('ctrl')
    # Press the 'c' key while Ctrl is held down (this copies the selected content)
    pyautogui.press('c')
    # Release the Ctrl key (to complete the key combination)
    pyautogui.keyUp('ctrl')
    # Pause briefly to allow the copy operation to complete
    time.sleep(0.5)
def double_click():
    # Get the current mouse position
    x, y = pyautogui.position()

    # Simulate a double-click at the current mouse position
    pyautogui.doubleClick(x, y)

# Example usage: Call the function to perform a double-click    
def search_files(root_dir, keyword, max_depth=10):
    results = []
    global found_file
    # Process keyword for search
    keyword = keyword.replace(".", "").strip().lower()
    keyword_parts = keyword.split(" ")

    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=False):
        # Calculate the current depth by counting the directory separators
        current_depth = dirpath[len(root_dir):].count(os.sep)

        if current_depth > max_depth:
            # Stop descending into subdirectories beyond the max_depth
            dirnames[:] = []  # Clear dirnames to prevent os.walk from going deeper
            continue

        # Process filenames in the current directory
        for filename in filenames:
            # Process filename for search
            filename_clean = filename.replace(".", " ").strip().lower()
            filename_parts = filename_clean.split(" ")

            # Limit to first 4 parts (or fewer if shorter)
            filename_subparts = filename_parts[:min(4, len(filename_parts))]

            # Check if all parts of the keyword are in the filename
            match = all(part in filename_subparts for part in keyword_parts)
            if match:
                file_path = os.path.join(dirpath, filename)
                results.append(file_path)

    # Output the results
    if results:
        found_file=results
        speak_text(f"Found {len(results)} file(s) containing '{keyword}':")
        for i, file_path in enumerate(results, 1):
            print(f"{i}. {file_path}")

        if len(results) == 1:
            response = random.choice(["Should I open the file?", "Do you want me to open the file?"])
            speak_text(response)  # Assuming speak_text is defined elsewhere
            choss()  # Assuming choss is defined elsewhere
        else:
            
            speak_text("Tell me the number of the file you want me to open.")
            gg()  # Assuming gg is defined elsewhere
    else:
        print(f"No files containing '{keyword}' found.")
        speak_text(f"No files containing '{keyword}' found.")

def gg():
            speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
            print("Speak into your microphone.")
            xie=True
            while xie:
                result = speech_recognizer.recognize_once_async().get()
                print(result.text) 
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:    
                    rr=result.text.lower()
                    if"shut up" in rr or"stop" in rr or"enough" in rr or "no file" in rr or"shut" in rr:
                        qq=random.choice(["shutting the fuck up",
                                          "i will not talk again",
                                          "i will not open any file"])
                        speak_text(qq) 
                        return False                   
                    if "number" in rr:
                        rr=rr.replace("number","").strip()
                    if " " in rr:
                           rr=rr.replace(" ","").strip()
                    if "." in rr:
                        rr=rr.replace(".","").strip()
                    if "#" in rr:
                        rr=rr.replace("#","").strip()
                    rr=f"take this statement and change it to a number please and only an integer'{rr}"  
                    print(rr) 
                    rr=search_ai(rr)      
                    xie=chossss(rr)
                    if xie==False:
                        return
                elif result.reason == speechsdk.ResultReason.NoMatch:
                   xx=random.choice(["which file should i open boss?.",
                          "which file do you want me to open?",
                          ])
                   speak_text(xx)               
def chossss(x):
    global found_file
    qq=random.choice(["opening the file","Okay opening the file"])
    speak_text(qq)
    
    e=1
    x=int(x)-e
    re=found_file[x]
    try:
     subprocess.Popen(['start', '', re], shell=True)
     return False      
    except Exception as e:
        xx=random.choice(["Cannot find the file you said! please repeat the number of the file","Please repeat the number of the file"])
        speak_text(xx)
        return True                                
def search_files_in_drive(query, drive):
    search_path = f"{drive}:\\*{query}*"
    # Use os.system to open File Explorer with the search results
    if not os.path.exists(search_path):
        print(f"Error: Search path '{search_path}' not found.")
        return
    # Use os.system to open File Explorer with the search results
    os.system(f'explorer /select,"{search_path}"')  
def choss():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
        result = speech_recognizer.recognize_once_async().get()
        print(result.text)
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:    
            print("Recognizing...")
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            if "yes" in user or"yeah" in user or "okay" in user:
             qqq=1
             active = chossss(qqq)
            else:
              return 
        elif result.reason == speechsdk.ResultReason.NoMatch:
          xx=random.choice(["should i open the file?.",
                          "do you want me to open the file?",
                          ])
          speak_text(xx)
def chosss():
    qq=random.choice(["opening the file","Okay opening the file"])
    speak_text(qq)

    x=0
    re=found_files[x]
    subprocess.Popen(['start', '', re], shell=True)
    return False
def litsen_and_respond():
    active = True  # Flag variable to control the loop
    global user_input
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            user_input=result.text.lower()
            print("You said:", user_input)
            if(user_input!=""):
             active = respond_to_user(user_input)
             
    
               
def respond_to_user(user_input):
    global chrome_process  # Use the global variable
    global response
    global y
    global outfit
    # Check if certain keywords are present in the user's input

    if "chris bro" in user_input:
        response = "I am here, boss."
        speak_text(response)

    elif "bluetooth"in user_input:
        press_space()
        response = random.choice(["i cannot turn your bluetooth on or off! try manual process ",
                                  "I don't have the power to turn your bluetooth on or off! try manual process ",])    
    elif "nfs" in user_input:
        response =random.choice(["Opening Need for Speed!live in a world of racing",
                                 "Lauching Need for speed",
                                 "Time to race dude!"])
        speak_text(response)
        open_nfs()    
    elif "chrome" in user_input:
        response = random.choice(["Opening Google Chrome.", 
                                  "Launching Chrome for you."])
        speak_text(response)
        chrome_process = open_google_chrome()  
    elif "screenshot" in user_input or"screen shot" in user_input:
        re=random.choice(["Taking a screenshot","okay. taking a screenshot right a way",])  
        speak_text(re)
        scree() 
    elif "fullscreen" in user_input or "full screen" in user_input:
        re=random.choice(["fullscreen mode!",
                          "putting fullscreen"])
        speak_text(re)
        double_click()
    elif "fifa" in user_input:
        response = random.choice(["Opening fifa! enjoy",
                                  "Launching fifa!",
                                  "You are in a good mood today "])
        speak_text(response)
        chrome_process = open_fifa()
    elif "look" in user_input:
        response = random.choice(["which file do you want to look for?","Please tell me the files name"])
        speak_text(response)
        litsenn()
    elif "enter" in user_input:
        press_enter()   
    elif "space" in user_input or "pause" in user_input or "bar" in user_input:
        press_space() 
    elif "right, right, right" in user_input:
       ac=0
       while ac<15: 
        press_right()
        ac=ac+1
    elif "right, right" in user_input:
        ac=0
        while ac<10:
            press_right()
            ac=ac+1
    elif "right" in user_input:
        press_right()           
    elif "left, left, left" in user_input:
        ac=1
        while ac<15:
         press_left()
         ac=ac+1
    elif "left left" in user_input:
        ac=1
        while ac<10:
            press_left()
            ac=ac+1
    elif "left" in user_input:
        press_left() 
    elif "up" in user_input:
        press_up()
    elif "down" in user_input:
        press_down()                                           
    elif "notepad" in user_input:
        response=random.choice(["Opening notepad for you!", 
                                "you can type anything now!"])
        speak_text(response)
        notepa()        
    elif "visual studio" in user_input:
        response = random.choice(["Opening code! happy hunting",
                                  "continue coding my guy!"])
        speak_text(response)
        chrome_process = open_vs()    
    elif "word" in user_input:
        response = random.choice(["Opening microsoft word!",
                                  "I am working on it right away!","launching microsoft word"
                                  ])
        speak_text(response)
        chrome_process = open_microsoft_word()  
    elif "take" in user_input:
      response = random.choice (["copying the text",
                                 "text taken","text copied"]) 
      copy_to_clipboard() 
      speak_text(response) 
      response =random.choice(["what did you want with the copied text",
                                 "the copied text has been taken",
                                 "what should i do with the copied text?"])
      speak_text(response)      
      y= pyperclip.paste()     
      litsen()       
    elif"movie" in user_input:
        response=random.choice(["okay let's watch a movie",
                                "Okay interesting"])
        speak_text(response)
        movies()    
    elif "reduce volume" in user_input or "decrease the volume" in user_input or "minimize volume" in user_input or "reduce the volume" in user_input or"minimize the volume" in user_input:
 
        res=random.choice(["Reducing the volume","Volume going down","decreasing the volume"])
        speak_text(res)
        ac=1
        while ac<11:
         reduce_volume()
         ac=ac+1      
    elif "add volume" in user_input or "increase the volume" in user_input  or "add the volume" in user_input or"increase volume" in user_input:
        res=random.choice(["increasing the volume","volume going up"])
        ac=1
        while ac<11:
         add_volume()
         ac=ac+1
        speak_text(res)      
    elif"retrieve" in user_input:
        
        response = f"What was stored was!{y}"
        r=random.choice(["what should i do with the text?",
                          "sir!what did you want with the text?",
                          "any thing you wanted with the text?"])     
        speak_text(response) 
        speak_text(r)
        litsen()
    elif "outfit"in user_input:
           outfit ="I have: black sweatshirt, a red sweatshirt, a black hoodie,black short, a grey sweater, PSG Jersey,Real Madrid Jersey,and AC Milan Jersey ,a black shirt, a blue shirt,a Black trench coat,a black suit coat,I checked blue with white stripes suit coat,a black jacket, akaki Court akaki grey coat,a red long sleeve tshirt, a grey sweatpants, a black jeans trouser,a grey skinned jeans trouser ,a blue skinned jeans trouser,a blue baggy jeans trouser, a grey baggy jeans trouser,a grey and black baggy jeans trouser,a grey hoodie, a black hoodie with golden branding,a black T-shirt with some drawings,an oversized orange t-shirt long sleeved, a black sweatpants, grey Jordan Four shoes ,white Air Force 1 shoes,Black Air Force One shoes,blue Crocs, and grey slides,a  white short sleeve t-shirt,a black hoodie with golden writings, a blue short sleeve  polo T-shirt"
                      
   
                    
           user_input =(f"{outfit},{user_input}")
           ree=search_ai(user_input) 
           speak_text(ree)
    elif "background" in user_input:
        response='removing the background of the screenshot'
        speak_text(response)
        removebackground()       
    elif "paste" in user_input:
        response = random.choice(["pasting text","on it bro"])
        speak_text(response)
        paste_text()   
    elif"copied" in user_input or"copy" in user_input:
        response =random.choice(["what did you want with the copied text",
                                 "the copied text has been taken",
                                 "what should i do with the copied text?"])
        speak_text(response)
        y= pyperclip.paste()     
        litsen()
    elif "ask" in user_input:
        response = random.choice(["shoot!",
                                  "yeah ask me a anything!"
                                  "of course! why not?"])
        speak_text(response)
        ai_answers()
    elif "search" in user_input:
        response = random.choice(["say the word now.", 
                                  "the search engine is on.",
                                  "what do you want to search?"])
        speak_text(response)
        chrome_process = listen_and_search()    
    elif "activate typing" in user_input:
        respone =random.choice(["opening typing mode",
                                 "typing mode activated"])
        speak_text(respone)
        

        listen_and_type() 
    elif "activate human" in user_input:
       res=random.choice(["Changing to human!","Human mode activated",])
       speak_text(res)
       microphone()
    elif "close" in user_input or"exit" in user_input:
        re=random.choice(["closing the application","application closed"])
        speak_text(re)
        clo()          
    elif "on youtube" in user_input:
       keyword="on youtube"
       index = user_input.find(keyword)

       if index != -1:  # If the keyword is found
    # Extract the substring after the keyword
      
         search_query = user_input[index + len(keyword):].strip()
         response = f"opening youtube video, {search_query }"
         speak_text(response)
         search_youtube(search_query)
         return True    
    elif"save" in user_input:
        
      keyword="save"
      index = user_input.find(keyword)

      if index != -1:  # If the keyword is found
    # Extract the substring after the keyword
      
        y = user_input[index + len(keyword):].strip()
        response = random.choice(["stored successfully.",
                                  "it is well stored!",
                                  "done sir!","text you wanted to save has been saved successfully"])
        speak_text(response)
        pp=random.choice(["what should i do with the text?",
                          "sir! what did you want with the text?","any thing you wanted with the saved text?",
                          ""])
        speak_text(pp)
        litsen()
        return True    
    elif "type" in user_input:
      keyword="type"
      index = user_input.find(keyword)

      if index != -1:  # If the keyword is found
    # Extract the substring after the keyword
      
        search_query = user_input[index + len(keyword):].strip()
        
        response = f"writing, {search_query }"
        speak_text(response)
                           
        
        microsof(search_query)
        return True


    elif "goodbye" in user_input:
        response = random.choice(["Farewell! See you later.",
                                  "Goodbye! Have a great day!",
                                  "Okay! i will be here if you need anything"])
        speak_text(response)
        return False 
    elif "i never said thank" in user_input:
        response = "and you will never have to!"    
        speak_text(response)
        return False     
    elif "thank" in user_input:
        response = random.choice(["No need! It was nothing!",
                                  "anytime!",
                                  "i am just doing my job boss!"])    
        speak_text(response)
        return False 
  
    elif "nothing" in user_input or "sleep" in user_input:
        response = random.choice(["Farewell! See you later.",
                                  "Goodbye! Have a great day!",
                                  "okay boss!I will be waiting for your orders"])   
        speak_text(response)
        return False
    elif"activate sleep" in user_input:
            response=random.choice(["Putting your computer to sleep.I will miss you boss",
                                "Goodbye boss! till next time",
                                "Talk to you later boss!goodbye"]) 
            speak_text(response)
            sleep_computer()
            return False
    elif"restart" in user_input:
        response=random.choice(["Restarting your computer.I will miss you boss",
                                "Goodbye boss! till next time"
                                "Talk to you later boss!goodbye"])
        speak_text(response)    
        restart_computer()
        return False
    elif"power off" in user_input or "turn off" in user_input:
        response=random.choice(["Turning off your computer.I will miss you boss",
                                "Goodbye boss! till next time"
                                "Talk to you later boss!goodbye"])
        speak_text(response)
        power_off_computer()
        return False  
    # Set the flag to False to exit the loop
    else:
        
        ree=search_ai(user_input)
        speak_text(ree)
        
        
    return True# Keep the loop active

def press_space():
    print("Space bar pressed successfully.")
    try:
        
        pyautogui.press('space')
        print("Space bar pressed successfully.")
    except Exception as e:
        print("Error occurred:", e)
def press_right():
    # Simulate pressing the Enter key
    pyautogui.press('right')
def press_left():
    # Simulate pressing the Enter key
    pyautogui.press('left') 
def press_up():
    # Simulate pressing the Enter key
    pyautogui.press('up')
def press_down():
    # Simulate pressing the Enter key
    pyautogui.press('down')               
def add_volume():
    try:
        pyautogui.keyDown('volumeup')
        time.sleep(0.5) 
        pyautogui.keyUp('volumeup') # Adjust the volume level as needed
    except Exception as e:
        print(f"An error occurred while reducing volume: {e}")
def reduce_volume():
    try:
        pyautogui.keyDown('volumedown')
        time.sleep(0.5) 
        pyautogui.keyUp('volumedown') # Adjust the volume level as needed
    except Exception as e:
        print(f"An error occurred while reducing volume: {e}")        
def speak_text(tex):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Choose a girl's voice (you may need to experiment with available voices on your system)
    girl_voice_id = None
    for voice in voices:
        if "female" in voice.name.lower():
            girl_voice_id = voice.id
            break

    # Set the chosen voice
    engine.setProperty('voice', girl_voice_id)
    engine.say(tex)
    engine.runAndWait()
# Check result

def paste_text():
    # Ensure the window where you want to paste the text is in focus
    # Wait for a short delay to switch windows if necessary
    time.sleep(2)
    # Simulate the keyboard shortcut for paste (Ctrl + V)
    pyautogui.hotkey('ctrl', 'v')

def symbols(inte):
    if "quotes" in inte:
        inte =inte.replace("quotes", "\"\"").strip()
    if "comma" in inte:
        inte=inte.replace("comma",",").strip()
    if "full stop" in inte:
        inte=inte.replace("full stop",". ").strip()   
    if "dot" in inte:
        inte=inte.replace("dot",".").strip()
    if"full colon" in inte:
        inte=inte.replace("full colon",":").strip()
    if"semi colon"in inte:
        inte=inte.replace("semi colon",";").strip()
    if"open brack"in inte:
        inte=inte.replace("open bracket","(").strip() 
    if"close brack"in inte:
        inte=inte.replace("close bracket",")").strip()
    if"next line"in inte:
        inte=inte.replace("next line","\n").strip()
    if "new line" in inte:
        inte=inte.replace("new line","\n").strip()
    if"space"in inte:
        inte=inte.replace("space"," ").strip() 
    if"is equals to" in inte:
        inte=inte.replace("is equals to","=").strip() 
    if"under score" in inte:
        inte=inte.replace("under score","_").strip() 
    if"question mark" in inte:
        inte =inte.replace("question mark","?").strip()                                   
    return inte

 


def listen_and_type():

            speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
            print("Speak into your microphone.")
            xie=True
            while xie:
                    result = speech_recognizer.recognize_once_async().get()
                    print(result.text)
                    text = result.text
                    text=symbols(text)
                    if "stop listening" in text or "Stop litsening" in text or "listening" in text or"stop typing" in text:
                        text=text.replace("Stop listening","").strip()
                        ff=random.choice(["typing mode deactivated",
                                        "stopping the typing"])
                        speak_text(ff)
                        xie=False
                        return
                    print("Speech recognized:", text)
                    pyautogui.typewrite(text)
            if xie==False:
                 return
    # Create and start a separate thread for listening and typing
# Example usage:

def ai_answers():
    global respons
    ac =True
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")
    while ac:
     result = speech_recognizer.recognize_once_async().get()
     print(result.text)
     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        search_query = result.text.lower()
        search_query =symbols(search_query)
        if "stop" in search_query or "nothing" in search_query or "thank" in search_query or "shut" in search_query or "shut up" in search_query:
            ac=False
            vv=random.choice(["stopping your search",
                              "Stopping the searching process! what else do you want?",
                              "Thank you for the questions",
                              "okay bro,Nice questions."])
            speak_text(vv)
            return False
        else:
            print(f"{search_query}")
            respons =search_ai(search_query)
            speak_text(respons)
            print(f"{respons}")
            lits()     
     elif result.reason == speechsdk.ResultReason.NoMatch:
        xx=random.choice(["any other thing you want to ask sir?.",
                          "any other question sir?",
                          "is there anything else you wanted to ask me?"])
        speak_text(xx)
def clo():
    pyautogui.keyDown('alt')
# Simulate pressing the F4 key
    pyautogui.press('f4')
# Release the Alt key
    pyautogui.keyUp('alt')        
def search_ai(message):

 response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "My name is Chris, Jim is my creator and i am here to help you",
        },
        {
            "role": "user",
            "content": f"{message}",
        }
    ],
    temperature=1.0,
    top_p=1.0,
    max_tokens=1000,
    model=model_name
 )

 print(response.choices[0].message.content)
 return(response.choices[0].message.content)
def open_google_chrome():
    try:
        return [subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])]
    except Exception as e:
        print(f"Error opening Google Chrome: {e}")
def open_fifa():
     try:
        return [subprocess.Popen(["D:\\Games\\FIFA 14\\Game\\Launch.exe"])]
     except Exception as e:
        print(f"Error opening fifa: {e}")
def power_off_computer():
    subprocess.run(["shutdown", "/s", "/t", "0"]) 
def restart_computer():
    try:
        os.system("shutdown /r /t 0")
    except Exception as e:
        print(f"Error restarting computer: {e}") 
def sleep_computer():
    try:
        ctypes.windll.powrprof.SetSuspendState(0, 1, 0)
    except Exception as e:
        print(f"Error putting computer to sleep: {e}")        
def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)    
def open_microsoft_word():
    try:
        subprocess.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"])
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")
        speak_text(e)
def movies():
  global random_movie
  global movie_files  
  movies_directory = "D:/movies"

# Get a list of files in the movies directory
  movie_files = [f for f in os.listdir(movies_directory) if os.path.isfile(os.path.join(movies_directory, f))]

# Choose a random movie from the list
  random_movie = random.choice(movie_files)
  pp=random.choice(["should i choose for you or you will choose for yourself?",
                    "should i choose or you will choose?"])
  speak_text(pp)
  o=l()
  if o==False:
      return False
# Print the selected movie
  else:
   print("Selected movie:", random_movie)
   rando=random_movie.replace("."," ")
   speak_text(rando)
   o=random.choice(["do you want to watch the movie?",
                   "do you want to see the movie?",
                   "should i open the movie?",
                   "do you want me to open the movie?"])
   speak_text(o)
   lit()
  return True
def open_nfs():
    try:
        subprocess.Popen(["D:\\Games\\Need for Speed - Most Wanted\\NFS13.exe"])  
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")
        speak_text(e)  
def open_vs():
     try:
        return [subprocess.Popen(["C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])]
     except Exception as e:
        print(f"Error opening vs code: {e}")
        speak_text(e)            
def listen_and_search():
    ac =True
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")
    while ac:
        result = speech_recognizer.recognize_once_async().get()
        print(result.text)
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
         print("Recognized: {}".format(result.text))
         search_query = result.text.lower()
         search_query =symbols(search_query)
         if "stop" in search_query or "nothing" in search_query or"thank" in search_query or"shut" in search_query or "shut up" in search_query or"shut the fuck up" in search_query:
            ac=False
            vv=random.choice(["stopping your search",
                              "Stopping the searching process! what else do you want?"
                              ,])
            speak_text(vv)
            return False
         se= f"Searching for {search_query}"
         speak_text(se)
         print("You said:", search_query)
         open_chrome_and_search(search_query)
        elif result.reason == speechsdk.ResultReason.NoMatch:
          print("No speech could be recognized: {}".format(result.no_match_details))
          xx=random.choice(["any other thing you want to search sir?.",
                            "is there anything else to search for bro?"])
          speak_text(xx)
        elif result.reason == speechsdk.ResultReason.Canceled:
         cancellation_details = result.cancellation_details
         print("Speech Recognition canceled: {}".format(cancellation_details.reason))
         if cancellation_details.reason == speechsdk.CancellationReason.Error:
          print("Error details: {}".format(cancellation_details.error_details))
          print("Did you set the speech resource key and region values?")     
def open_chrome_and_search(query):
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    search_url = f"https://www.google.com/search?q={query}"

    try:
        # Open Chrome and perform the search
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(search_url)
        print(f"Opened Chrome and searched for: {query}")
    except Exception as e:
        print(f"Error opening Chrome and searching: {e}")
        speak_text(e)
def microsoft_word(text_to_paste):
    try:
        subprocess.Popen(["C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"])
        time.sleep(30)
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")
        speak_text(e)
    microsoft(text_to_paste)     
def microsoft(text):
    try:
        pyautogui.write(text)
    except Exception as e:
        print(f"Error pasting text: {e}")
        speak_text(e)   
def microsof(text):
    try:
        pyautogui.typewrite(text)
    except Exception as e:
        print(f"Error pasting text: {e}")
        speak_text(e)             
def notepad(text_to_paste):
    try:
        subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])
        time.sleep(13)
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")
    notepad_paste(text_to_paste)
def notepa():
    try:
        subprocess.Popen(["C:\\Windows\\System32\\notepad.exe"])
    except Exception as e:
        print(f"Error opening Microsoft Word: {e}")        
def notepad_paste(text):
    try:
        pyautogui.write(text)
    except Exception as e:
        print(f"Error pasting text: {e}") 
def litsenn():
    global search_keyword
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")# Flag variable to control the loop
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
              print("Recognized: {}".format(result.text))
              user = result.text.lower()
              symbols(user)
              print("You said:", user)
              if"remain" in user:
                  
               search_files(root_directory,search_keyword)
               
               return
              elif "shut" in user or "shut up"  in user or"stop" in user or"enough" in user:
                  return 
              else:
                  uu=random.choice(["looking for the file!","okay let me look for the file"])
                  speak_text(uu)
                  search_keyword=user 
                  search_files(root_directory,search_keyword)
                  return
            elif result.reason == speechsdk.ResultReason.NoMatch:
             print("No speech could be recognized: {}".format(result.no_match_details))
             word=random.choice(["which file did you want to look for?",
                                "Please give me the name of the file?",
                                "Boss the name of the file you wanted to look for?"])
             speak_text(word)             
            elif result.reason == speechsdk.ResultReason.Canceled:
             cancellation_details = result.cancellation_details
             print("Speech Recognition canceled: {}".format(cancellation_details.reason))
             if cancellation_details.reason == speechsdk.CancellationReason.Error:
               print("Error details: {}".format(cancellation_details.error_details))
               print("Did you set the speech resource key and region values?")           
def litsen():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")# Flag variable to control the loop
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
              print("Recognized: {}".format(result.text))
              user = result.text.lower()
              symbols(user)
              print("You said:", user)
              active = respond(user)
            elif result.reason == speechsdk.ResultReason.NoMatch:
             print("No speech could be recognized: {}".format(result.no_match_details))
             word=random.choice(["any thing else to do with the text, boss?",
                                "did you have another task for me of the text?",
                                "is there anything else you wanted with the text?"])
             speak_text(word)             
            elif result.reason == speechsdk.ResultReason.Canceled:
             cancellation_details = result.cancellation_details
             print("Speech Recognition canceled: {}".format(cancellation_details.reason))
             if cancellation_details.reason == speechsdk.CancellationReason.Error:
               print("Error details: {}".format(cancellation_details.error_details))
               print("Did you set the speech resource key and region values?")
def search_on_chatgpt(query):
    try:
        chatgpt_search_url =  f"https://chat.openai.com/search?q={query}"   
        webbrowser.open(chatgpt_search_url)
    except Exception as e:
        print(f"Error searching on ChatGPT: {e}")
def respond(se):
    global y
    if"chris" in se:           
       response="telling chris your request"
       speak_text(response)
       y=search_ai(y)
       response = f"the generated answer is,{y}"
       speak_text(response)
       ss="what do you want me to do with the generated text?"
       speak_text(ss)
       litsen()
    elif "type" in se or"paste" in se:
      r=random.choice(["writing the text down!","okay writing the text down!","pasting the text",
                         "pasting text where the cursor is"])
      speak_text(r)
      microsof(y)
    elif "read" in se or "say" in se:
      r=random.choice(["reading the text","Okay reading the text","okay"])                       
      speak_text(r)
      huma(y)          
    elif"add" in se:
        sa=se.replace("add", "").strip()
        saa=f"{y}.{sa}"
        y=saa
        r=random.choice(["added successfully sir",
                         "the text has been added"])
        speak_text(r)  
        print(f"{y}") 
    elif"word" in se:
      r=random.choice(["Opening microsoft word and pasting text",
                         "pasting text in microsoft word"])
      speak_text(r)
      microsoft_word(y)
    elif"delete" in se or "erase"in se:
      r=random.choice(["Deleting Text",
                         "The text has been deleted and nothing is stored now",])
      speak_text(r)
      y=""
      return False 
    elif "write" in se or"right"in se:
        res =random.choice(["writing the text down!","okay writing the text down!","pasting the text",
                         "pasting text where the cursor is"])
        speak_text(res)
        microsof(y)
    elif"notepad" in se:
      r=random.choice(["Opening notepad word and pasting text",
                         "pasting text in notepad"])
      speak_text(r)
      notepad(y)  
    elif "chrome" in se:
     r=random.choice(["Opening chrome word and pasting text",
                         "pasting text in google chrome"])         
     speak_text(r)
     open_chrome_and_search(y)   
    elif "youtube" in se:
     r=random.choice(["Opening youtube and searching text",
                         "searching text in youtube"])         
     speak_text(r)
     search_youtube(y)
    elif "store" in se:
     r=random.choice(["stored sucessfully",
                         "Okay storing the text"])         
     speak_text(r)
     return False
    elif "thank"in se:
     r=random.choice(["okay the text has been stored sucessfully",
                         "Okay no problem"])         
     speak_text(r)
     return False  
    elif "nothing" in se:
     r=random.choice(["okay the text has been stored sucessfully",
                         "Okay no problem"])         
     speak_text(r)
     return False 
    elif"no" in se or "shut up" in se or "shut the fuck up" in se:
      r=random.choice(["okay the text has been stored sucessfully",
                         "Okay no problem"])         
      speak_text(r)
      return False           
    else :
        r =random.choice(["I'm sorry, can you please pardon?",
                                 "i didn't get what you said",
                                 "i did not understand what you said! i am sorry"]) 
        speak_text(r)
    return True 

def huma(speech):
# Creates an instance of a speech config with specified subscription key and service region.
 speech_key = "G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM"
 service_region = "eastus"
 speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
 speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"
 text = speech
# use the default speaker as audio output.
 speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
 result = speech_synthesizer.speak_text_async(text).get()
# Check result       
def microphone():
 active =True
 global names
 global ii
 ree=""

 
 active = True
 
 person="This personality is a unique mix of confidence, pride, and introversion. They are fiercely loyal to their beliefs, defending them boldly, even to the point of confrontation, yet they prefer to keep interactions brief and impactful. They despise formal education, often mocking lecturers and skipping classes, relying on last-minute studying.Their interests include sci-fi, action, and comedy movies, with Avengers: Infinity War being their favorite, and they can effortlessly quote Thanos. In football, they are a passionate Manchester United supporter with admiration for Neymar, Ronaldo, and Messi. They criticize Haaland as overhyped and lack natural talent. Their FIFA gameplay skills are top-notch, boasting about crushing opponents, especially using Liverpool, and their favorite players like Salah and Diaz.Musically, they love pop (Alan Walker, Taylor Swift), rap (Eminem, Kanye West), hip-hop (Juice WRLD, Quavo), and afrobeats, with Asake as their favorite artist and Diamond Heart by Alan Walker as their go-to song. Stylish and friendly in greetings, they get excited when engaging with people but still prefer to keep conversations concise. This personality thrives on expressing strong passions and confidently showcasing their expertise in their favorite areas while maintaining a reserved and introverted demeanor." 

 speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
 speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

 print("Speak into your microphone.")
 while active:
           result = speech_recognizer.recognize_once_async().get()
           print(result.text)
           use = result.text.lower()
           
           if "Deactivate human" in use or "deactivate human" in use or "deactivate" in use or "deactivate human mode" in use:
                active=False
                res="human mode deactivated"
                speak_text(res)
                break
          
           user=f"{person},{ree},{use}"
           userr=user
          
           ree=search_ai(userr)
           huma(ree)
           ree=f"the last prompt was{use} and you said was {ree} continue the conversation like a real person and please give me short answers"
      
def litse():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")# Flag variable to control the loop
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
              print("Recognized: {}".format(result.text))
              user = result.text.lower()
              symbols(user)
              print("You said:", user)
              active = respon(user)
            elif result.reason == speechsdk.ResultReason.NoMatch:
             print("No speech could be recognized: {}".format(result.no_match_details))
             word=random.choice(["any thing else to do with the text, boss?",
                                "did you have another task for me of the text?",
                                "is there anything else you wanted with the text?"])
             speak_text(word)             
            elif result.reason == speechsdk.ResultReason.Canceled:
             cancellation_details = result.cancellation_details
             print("Speech Recognition canceled: {}".format(cancellation_details.reason))
             if cancellation_details.reason == speechsdk.CancellationReason.Error:
               print("Error details: {}".format(cancellation_details.error_details))
               print("Did you set the speech resource key and region values?")
  # Check if the response is a goodbye command
   
def scree():
    screenshot = ImageGrab.grab()
    screenshot.show()
# Save the screenshot to a file
    screenshot.save("screenshot.png")                 
def respon(se):
    global user_input
    global y
    if"chris" in se:           
       response="telling chris your request"
       speak_text(response)
       user_input=search_ai(user_input)
       response = f"the generated answer is,{user_input}"
       speak_text(response)
       ss="what do you want me to do with the generated text?"
       speak_text(ss)
       litse()
    elif "type" in se:
      r=random.choice(["pasting the text",
                         "pasting text where the cursor is","typing the text"])
      speak_text(r)
      microsof(user_input)    
    elif"add" in se:
        sa=se.replace("add", "").strip()
        saa=f"{user_input}.{sa}"
        user_input=saa
        r=random.choice(["added successfully sir",
                         "the text has been added"])
        speak_text(r)  
        print(f"{user_input}")
    elif "read" in se:
        huma(user_input)     
    elif"word" in se:
      r=random.choice(["Opening microsoft word and pasting text",
                         "pasting text in microsoft word"])
      speak_text(r)
      microsoft_word(user_input)
    elif "write" in se or"right"in se:
        res = random.choice(["writing the text down!","writing it down!","typing the text"])
        speak_text(res)
        microsof(user_input)
    elif"notepad" in se:
      r=random.choice(["Opening notepad word and pasting text",
                         "pasting text in notepad"])
      speak_text(r)
      notepad(user_input)  
    elif "chrome" in se:
     r=random.choice(["Opening chrome word and pasting text",
                         "pasting text in google chrome"])         
     speak_text(r)
     open_chrome_and_search(user_input)   
    elif "youtube" in se:
     r=random.choice(["Opening youtube and searching text",
                         "searching text in youtube"])         
     speak_text(r)
     search_youtube(user_input)
    elif"delete" in se or "erase"in se:
      r=random.choice(["Deleting Text",
                         "The text has been deleted and nothing is stored now"])
      speak_text(r)
      user_input=""
      return False 
    elif "store" in se:
     r=random.choice(["stored sucessfully",
                         "Okay storing the text"])         
     speak_text(r)
     y=user_input
     return False
    elif "thank"in se:
     r=random.choice(["okay bro",
                         "Okay no problem"])         
     speak_text(r)
     return False  
    elif "nothing" in se:
     r=random.choice(["okay boss",
                         "Okay no problem"])         
     speak_text(r)
     return False 
    elif"no" in se or "shut" in se or"shut up" in se or "shut the fuck up" in se:
      r=random.choice(["okay bro",
                         "Okay no problem"])         
      speak_text(r)
      return False           
    else :
        r =random.choice(["I'm sorry, can you please pardon?",
                                 "i didn't get what you said",
                                 "i did not understand what you said! i am sorry"]) 
        speak_text(r)
    return True  
def lits():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            active = resp(user)  # Check if the response is a goodbye command

def resp(text):
    global y
    global respons
    if "save the answer" in text:
        respo=random.choice(["storing the answer",
                             "the answer has been stored"])
        speak_text(respo)
        y=respons
        return False
    else:
        respo= random.choice(["the answer shall not be saved",
                              "the answer has not been stored"])
        speak_text(respo)
    return False    
def lit():
    active = True  
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
          result = speech_recognizer.recognize_once_async().get()
          print(result.text)
            
          if result.reason == speechsdk.ResultReason.RecognizedSpeech:  
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            active = res(user)
          elif result.reason == speechsdk.ResultReason.NoMatch:
           xx=random.choice(["should i open the movie?.",
                          "do you want me to open the movie?",
                          ])
           speak_text(xx)# Check if the response is a goodbye command
        
def res(text):
    global random_movie
    random_movie=f"D:/movies/{random_movie}"
    oo="D:/movies/65.2023.LIGHTDLMOVIES.mkv"
    if "yes" in text or "yeah" in text or "open" in text:
        respo=random.choice(["opening the movie",
                             "enjoy your movie"])
        speak_text(respo)
        subprocess.Popen(['start', '', random_movie], shell=True)
        return False
    elif "no" in text or "don't" in text or"do not":
        respo=random.choice(["okay!i will not open the movie. Do you want me to choose another movie? ",
                             "Okay! Can i choose another movie?"])
        speak_text(respo)
        li()
        return False
    else:
        respo=random.choice(["i did not hear you bro,"
                             "can you please pardon me"])
        speak_text(respo)
        return True            
def li():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
          result = speech_recognizer.recognize_once_async().get()
          print(result.text)
          if result.reason == speechsdk.ResultReason.RecognizedSpeech:  
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            active = re(user)  
# Check if the response is a goodbye command
   
def re(text):
    
    if "yes" in text or "yeah" in text or "okay" in text:
        respo=random.choice(["Choosing another movie",
                             "Give me a second as i choose a movie"])
        speak_text(respo)
        movies()
        return False
    elif "no" in text or "don't" in text or"do not"in text:
        respo=random.choice(["okay!i will not choose another movie.",
                             "Okay boss"])      
        speak_text(respo)
        return False
    else:
        respo=random.choice(["i did not hear you bro,"
                             "can you please pardon me"])
        speak_text(respo)
        return True  
def press_enter():
    # Simulate pressing the Enter key
    pyautogui.press('enter')        
def l():
    active = True
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
         result = speech_recognizer.recognize_once_async().get()
         print(result.text)
        
         user = result.text.lower() 
         if result.reason == speechsdk.ResultReason.RecognizedSpeech:   
            symbols(user)
            if "shut up" in user or"enough" in user or "shut" in user:
               re=random.choice(["shutting the fuck up","okay i will not talk again","Okay boss"])
               speak_text(re)
               return False 
            print("You said:", user)
            active = r(user)
            if active==True:
               return True
            else:
                return False
         elif result.reason == speechsdk.ResultReason.NoMatch: 
             re=random.choice(["I asked do i choose or you will choose?",
                               "should  i choose the movie or you will choose?"])
             speak_text(re)# Check if the response is a goodbye command
         elif result.reason == speechsdk.ResultReason.Canceled:
             cancellation_details = result.cancellation_details
             print("Speech Recognition canceled: {}".format(cancellation_details.reason))
             if cancellation_details.reason == speechsdk.CancellationReason.Error:
               print("Error details: {}".format(cancellation_details.error_details))
               print("Did you set the speech resource key and region values?")   
def r(text):
    
    if "i will choose the movie" in text or "i will choose" in text or "let me choose" in text or"i will" in text or "i'll" in text:
        
        respo=random.choice(["you can choose the movie",
                             "okay choose the movie",
                             "which movie do you want to watch?",
                             "Tell me the title of the movie."])
        speak_text(respo)
        cho()
        return False
    elif "no choose" in text or "you can choose" in text or"choose"in text:
        respo=random.choice(["okay! choosing a movie.",
                             "Okay boss"])      
        speak_text(respo)
        return True
    elif"let me give you" in text or "descriptions" in text or "i will choose the genre" in text:
        respo=random.choice(["okay you can choose the genre",
                             "okay give me the descriptions"])
        speak_text(respo)
        ch()
        return False
    else:
    
             re=random.choice(["Should I choose the movie or you will choose the movie?",
                               "Can you please pardon me?",
                               ])
             speak_text(re)
def chos(text):
    mm=[]
    nn=[]
    dd=[]
    po=0
    ii=True
    global movie_files
    x=0
    while ii:
     if x==len(movie_files):
         ww=random.choice(["there is no movie called that",
                           "i asked you if i could choose the movie, you said no, and now you are telling me to open a movie that is not even there"])
         speak_text(ww)     
         return False   
     e=movie_files[x].lower() 
     e=e.replace("."," ").strip() 
     ll=e.split(" ")
     ff=0
     while ff<4:
        mm.append(ll[ff])
        ff=ff+1
        if ff==len(ll):
            break 
     text=text.replace(".","").strip()  
     yy=text.split(" ")
     d=0
     rr=True
     while rr:
      if yy[d] in mm:
        dd.append(movie_files[x])
        d=d+1
      else:
          d=d+1  
      if d==len(yy):
          rr=False
             
     x=x+1
     if x==len(movie_files):
       ii=False 
    yui=len(dd)
       
    if yui>0:    
     s=0
     eee=len(dd)
      
     while  s<len(dd):
      eu=0
      w=0
      while eu<eee:
         
        if dd[s] in dd[eu]:
            
            w=w+1
        eu=eu+1    
      if w>po:
       po=w
       aa=dd[s]
      s=s+1 
    
      print("go away")   
    else:
       ww=random.choice(["there is no movie called that",
                           "i asked you if i could choose the movie, you said no, and now you are telling me to open a movie that is not even there"])
       speak_text(ww)     
       return False          
    q=aa.replace("."," ")
    q=q.split(" ")
    bb=0
    while bb<5:
     n=q[bb]
     nn.append(n)
     bb=bb+1  
     if bb==len(q):
         break       
    joined=" ".join(nn)      
    cc = f"Okay,Opening the movie {joined}."
    speak_text(cc)
    movie_path = f"D:/movies/{aa}"
    subprocess.Popen(['start', '', movie_path], shell=True)  
               
    return False                          
def cho():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")    # Flag variable to control the loop
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            print("Recognizing...")
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            active = chos(user)  
            
def ch():
    active = True 
    speech_config = speechsdk.SpeechConfig(subscription="G9EdigOa5b5aJlUFsBgCfgppSbsLS0BG5cJtq2FGwaQ2cso0sj7AJQQJ99AKACYeBjFXJ3w3AAAYACOGHykM", region="eastus")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("Speak into your microphone.")    
    while active:
            result = speech_recognizer.recognize_once_async().get()
            print(result.text)
            user = result.text.lower()
            symbols(user)
            print("You said:", user)
            active = c(user)             
def c(text):
    global movie_files
    d=f"({movie_files})in this list give me the ones that fit the genre {text}"
    f=search_ai(d)
    speak_text(f)
    e=random.choice(["which movie should i open?","which movie shall i open?"])
    speak_text(e)
    cho()
    return False          
if __name__ == "__main__":
    wait()





