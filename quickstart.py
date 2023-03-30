from __future__ import print_function

import datetime
import os.path
import json
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pygame import mixer
# import pytz

# If modifying these scopes, delete the file token.json.6
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    hoursNeeded = int(input("How many hours do you need from the start of your alarm to your first commitment?\n"))
    minsNeeded = int(input("How many minutes do you need from the start of your alarm to your first commitment?\n"))
    
    timeNeededinMins = int(hoursNeeded * 60 + minsNeeded)
        
    
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        json_object = json.dumps(events, indent = 4)

        with open("events.json", "w") as outfile:
            outfile.write(json_object)

        firstEvent = 2561
        for event in events:
            currEvent = event['start']['dateTime']
            if (event['kind'] == 'calendar#event'):
                timeString = str(currEvent)
                eventStartTime = timeString[11:13] + timeString[14:16]
                if (int(eventStartTime) < int(firstEvent)):
                    firstEvent = eventStartTime
                    firstEventInMins = (int(timeString[11:13]) * 60) + int(timeString[14:16])
                    
        alarmTimeInMins = firstEventInMins - timeNeededinMins
        minutes = int(alarmTimeInMins % 60)
        hours = int((alarmTimeInMins - minutes) / 60)
        alarmTime = str(hours) + ":" + (str(minutes)).zfill(2)

        print("Alarm will ring at", alarmTime)
        print(now)
        
        # Play alarm sound
        # mixer.init() 
        # sound=mixer.Sound("alarm-clock.wav")
        
        # soundTimeEnd = time.time() + sound.get_length()
        # while (time.time() < soundTimeEnd):
        #     sound.play()
        
        # Get the timezone object for New York
        # tz_NY = pytz.timezone('America/New_York') 

        # Get the current time in New York
        # datetime_NY = datetime.now(tz_NY)

        # Format the time as a string and print it
        # print("NY time:", datetime_NY.strftime("%H:%M:%S"))

        if not events:
            print('No upcoming events found.')
            return

    except HttpError as error:
        print('An error occurred: %s' % error)
        
    page_token = None

if __name__ == '__main__':
    main()
