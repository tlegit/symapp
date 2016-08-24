#===================================================================================   
#
# Date: August 23, 2016
# Author: The-Binh Le
# Usage:
#   > python app.py
#
#----------------------------------------------------------------------------------
#
# This script does the following:
# - checking required environment variables are set
#   GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, LCBO_API_KEY, APP_SECRET_KEY
#   + GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET can be obtained from Google web site
#   + LCBO_API_KEY can be obtained from lcboapi web site
#   + APP_SECRET_KEY can be set by user
#   If any of the above variables is not set, the execution aborts
# - authenticating user via Google account login using OAuth
# - retrieving data from LCBO such as stores, inventories and products
# 
# This script can also be deployed in a Docker container. Its Docker image has
# been built and loaded to Docker Hub.
#
#===================================================================================   

from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import os

# Set required environment variables
#
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
LCBO_API_KEY = os.getenv('LCBO_API_KEY')
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

if GOOGLE_CLIENT_ID == None or \
   GOOGLE_CLIENT_SECRET == None or \
   LCBO_API_KEY == None or \
   APP_SECRET_KEY == None:
   raise Exception("These environment variables must be set: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, LCBO_API_KEY, APP_SECRET_KEY")

# Redirect URI defined in Google OAUTH configuration
#
REDIRECT_URI = '/oauth-redirect'
 
# Program starts
#
app = Flask(__name__)
app.debug = True
app.secret_key = APP_SECRET_KEY
oauth = OAuth()
 
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
 
# Default URL (index)
#
@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    return redirect(url_for('lcbo_select'))

# URL for Login against Google authentication mechanism
#    
@app.route('/login')
def login():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)
 
# URL for Redirect from Google authentication
#
@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))

# Interface with LCBO API
#
@app.route('/lcbo_select')
def lcbo_select():
    return render_template('lcbo_select.html')

@app.route('/lcbo_list', methods=['POST', 'GET'])
def lcbo_list():
    import urllib2, json

    if request.method == 'POST':
       input = request.form
       req = urllib2.Request('https://lcboapi.com/'+input['drop-down-list'])
       req.add_header('Authorization', 'Token '+LCBO_API_KEY)
       data = json.load(urllib2.urlopen(req))
       result = data['result']
       return render_template("table.html",result=result)
 
# Main program
#
def main():
    app.run(host='0.0.0.0')
 

if __name__ == '__main__':
    main()

