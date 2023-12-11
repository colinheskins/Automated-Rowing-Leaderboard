import httpx
from flask import Flask, request
from threading import Thread
from urllib.parse import urlencode
import webbrowser
import os
import helpers
import asyncio

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
    app.run(port=80)

async def get_authorization_code():
    authorization_url = "https://log.concept2.com/oauth/authorize"
    params = {
        "client_id": helpers.client_id,
        "scope": "user:read,results:read",
        "response_type": "code",
        "redirect_uri": "https://cf35-2600-1700-6d90-dc70-a071-ae51-9061-cbf4.ngrok-free.app/callback",
    }
    authorization_url_with_params = f"{authorization_url}?{urlencode(params)}"
    webbrowser.open(authorization_url_with_params)

    print("Waiting for authorization callback...")
    while authorization_code is None:
        await asyncio.sleep(1)
    print(authorization_code)
    return authorization_code

async def start_auth():

    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Step 1: Get Authorization Code
    authorization_code = await get_authorization_code()

    # Wait for Flask server thread to finish
    flask_thread.join()

    return authorization_code

if __name__ == '__main__':
    # Use '0.0.0.0' to listen on all public IPs
    app.run(host='0.0.0.0', port=80)
