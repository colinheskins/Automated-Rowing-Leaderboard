import httpx
from flask import Flask, request
from threading import Thread
from urllib.parse import urlencode
import webbrowser
import os

#Done by chat gpt, not entirely sure whats going on here

app = Flask(__name__)
authorization_code = None
CLIENT_ID = os.getenv("client_id")

@app.route('/callback')
def callback():
    global authorization_code
    authorization_code = request.args.get('code')
    if authorization_code:
        return "Authorization Code Received. You can close this window."
    else:
        return "Error: No Authorization Code received."

def run_flask():
    app.run(port=5000)

def get_authorization_code(client_id, scope, response_type, redirect_uri):
    
    authorization_url = "https://log.concept2.com/oauth/authorize"
    
    # Prepare parameters for the authorization URL
    params = {
        "client_id": client_id,
        "scope": scope,
        "response_type": response_type,
        "redirect_uri": redirect_uri,
    }

    # Construct the authorization URL
    authorization_url_with_params = f"{authorization_url}?{urlencode(params)}"
    print(authorization_url_with_params)

    # Open the authorization URL in the default web browser
    webbrowser.open(authorization_url_with_params)

    # Wait for the Flask server to receive the callback
    print("Waiting for authorization callback...")
    while authorization_code is None:
        pass

    return authorization_code

async def startAuth():
    # Replace these with your actual client details
    client_id = "VczzsuzCOWWMfUkXarfHS9VWNYGLZdwl62yNQaNB"
    scope = "user:read,results:read"
    response_type = "code"
    redirect_uri = "http://localhost:5000/callback"

    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Step 1: Get Authorization Code
    authorization_code = get_authorization_code(client_id, scope, response_type, redirect_uri)
    return authorization_code
    # Wait for Flask server thread to finish
    flask_thread.join()

