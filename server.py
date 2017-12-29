import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.rest import Client
import twilio.twiml
from twilio.twiml.voice_response import Client, Dial, VoiceResponse

ACCOUNT_SID = 'ACe455245ec387876eca1ff1454e7cc0da'
API_KEY = 'SK15349df1ee7a09ec30d48b051ce34131'
API_KEY_SECRET = 'YWaCQpm8TY0VfDqn2TI3HkI6skYDMPY2'
PUSH_CREDENTIAL_SID = 'CR1b514b015c948d64b3890d5042a42352'
APP_SID = 'APe335e1d6e4058c61eb0fae904dbc4557'

CALLER_ID = 'quick_start'

app = Flask(__name__)

@app.route('/accessToken')
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)

  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  token = AccessToken(
	account_sid,
	api_key,
	api_key_secret,
	identity=request.args.get("identity"))
  token.add_grant(grant)

  return str(token.to_jwt())

@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  from_user = request.form['from']
  to_user = request.form['to']
  print from_user + "->" + to_user

#  resp = twilio.twiml.Response()
#  resp.say("This is ongoing call. Is this me who you looking for?")
  response = VoiceResponse()
  dial = Dial()
  dial.client(to_user)
  response.append(dial)
  return str(response)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have received your first inbound call! Good bye.")
  return str(resp)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
