'''Setting-up Oauth'''
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
# CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR,'client_secret_new.json')
def get_calendar_service(request):
	try:
		creds = None
	   # The file token.pickle stores the user's access and refresh tokens, and is
	   # created automatically when the authorization flow completes for the first
	   # time.
		token_dir = 'user_calendar_tokens/'
		curr_user_token_path_file = token_dir + 'token' + request.user.username + '.pickle'
		if os.path.exists(curr_user_token_path_file):
			with open(curr_user_token_path_file, 'rb') as token:
				creds = pickle.load(token)
	   # If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
	   			creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('client_secret_new.json',scopes=scopes)
				creds = flow.run_local_server(port=0)
	       # Save the credentials for the next run
			with open(curr_user_token_path_file, 'wb') as token:
				pickle.dump(creds, token)
	   #Creating a service object for using the API
		if build('calendar', 'v3', credentials=creds):
			service = build('calendar', 'v3', credentials=creds)
	   #creds are the credentials generated bu oauth 2.0 Flow.
		return service
	except Exception:
		return False
