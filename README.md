# rise-and-shine
* Alarm clock that connects to google calendar and automatically sets alarm based on user*given input of time needed in the morning before first event. 
* The goal is to prevent people from sleeping through their commitments, especially in the morning.

# What I Learned
* Python automated scripting
* Google Calendar API connection
* Utilizing audio in Python

## Quickstart (to run on personal machine)
* Clone repo and run on coding editor (must have Python installed)
* Install the Google client library for Python: `python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
* Install pygame library (plays alarm sound): `python3 -m pip install -U pygame --user`
* Authorize Google Calendar API by downloading oauth2l with `brew install oauth2l` (assumes Homebrew is installed)
* Run `oauth2l fetch --credentials credentials.json --scope adwords \ --output_format refresh_token` to authorize your Google Calendar
* `python3 quickstart.py` to run program
   * If python3 not installed, install python [here](https://www.python.org/downloads/)
