from pywizlight import wizlight, PilotBuilder
import asyncio
import closeCalls
import sys


lightOnDict = ["light on", "right on", "lay on", "lamp on"]
lightOffDict = ["light off", "right off" , "lay off", "let off", "led off", "let up", "lamp off"]


from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(message):
    engine = pyztsx3.init()
    engine.say(message)
    engine.runAndWait()



def execute(command, text):
    for phrase in lightOnDict:
        if phrase in command:
            light = wizlight("192.168.1.28")
            asyncio.run(light.turn_on(PilotBuilder()))

    for phrase in lightOffDict:
        if phrase in command:
            light = wizlight("192.168.1.28")
            asyncio.run(light.turn_off())
    
    if "exit" in command:
        print(text)
        sys.exit()    
    
    else:
        