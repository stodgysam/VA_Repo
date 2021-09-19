from pywizlight import wizlight, PilotBuilder
import asyncio
import speech_recognition as sr
import sys
import commands
        
lightOnDict = ["light on", "right on", "lay on", "lamp on"]
lightOffDict = ["light off", "right off" , "lay off", "let off", "led off", "let up", "lamp off"]
        
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        print(type(audio))
        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()


def tryGoodgle():

    WAKE = "howard"
    print("Start")

    for i = 1 to 3:
        print("Listening")
        text = get_audio()
        commands.execute(text)
        

        