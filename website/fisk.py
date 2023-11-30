import httpx
from flask import Flask, render_template, request
from threading import Thread
from urllib.parse import urlencode
import webbrowser
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
authorization_code = None
student_id = None

authorization_url = "https://log.concept2.com/oauth/authorize"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/callback')
def callback():
    global authorization_code, student_id
    authorization_code = request.args.get('code')
    student_id = request.args.get('student_id')
    if authorization_code and student_id:
        socketio.emit('auth_info', {'student_id': student_id, 'authorization_code': authorization_code})
        return "Authorization Code and Student ID received. You can close this window."
    else:
        return "Error: No Authorization Code or Student ID received."

@socketio.on('submit_student_id')
def handle_student_id(data):
    global student_id
    student_id = data['student_id']
    socketio.emit('student_id_received', {'student_id': student_id})

def run_flask():
    socketio.run(app, port=5000)

def get_authorization_code(client_id, scope, response_type, redirect_uri):
    global student_id

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
    while authorization_code is None or student_id is None:
        pass

    return student_id, authorization_code

async def startAuth():
    # Replace these with your actual client details
    client_id = "VczzsuzCOWWMfUkXarfHS9VWNYGLZdwl62yNQaNB"
    scope = "user:read,results:write"
    response_type = "code"
    redirect_uri = "http://localhost:5000/callback"

    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Step 1: Get Authorization Code
    student_id, authorization_code = get_authorization_code(client_id, scope, response_type, redirect_uri)
    return student_id, authorization_code

    # Wait for Flask server thread to finish
    flask_thread.join()


asyncio.run(startAuth)