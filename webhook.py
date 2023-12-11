from flask import Flask, request, jsonify
import json
from urllib.parse import urlencode
import webbrowser
import helpers
import worksheet
import helpers

logger = helpers.get_logger()

app = Flask(__name__)
authorization_code = None
# Load users from users.json
with open('users.json') as f:
    data = json.load(f)
    users = data.get('users', [])

@app.route('/webhook', methods=['POST'])
async def handle_webhook():
    # Verify that the request contains JSON data
    if request.is_json:
        data = request.json

        # Extract event type and result payload
        try:
            event_type = data['type']
            result = data['result']

        except KeyError as e:
            return jsonify({'error': f'Missing key in JSON payload: {str(e)}'}), 400

        # Handle different event types
        if event_type == 'result-added':
            # Logic for result-added event
            await handle_result_added(result)
        elif event_type == 'result-updated':
            # Logic for result-updated event
            handle_result_updated(result)


        # Respond with a success message
        return jsonify({'message': 'Webhook received successfully'}), 200
    else:
        # Respond with an error if the request does not contain JSON data
        return jsonify({'error': 'Invalid request format'}), 400
    
@app.route('/callback')
async def callback():
    global authorization_code
    authorization_code = request.args.get('code')
    if authorization_code:
        return "Authorization Code Received. You can close this window."
    else:
        return "Error: No Authorization Code received."

async def handle_result_added(result):
    user_id = result.get('user_id')
    time = result.get('time_formatted')
    distance = result.get('distance')

    if user_id is not None and time is not None and distance is not None:
        name = next((u for u in users if u['userid'] == int(user_id)), None)['name']
        print(f"New result added - Username: {name}, Time: {time}, Distance: {distance} meters")
        logger.info("Posting workout to worksheet")
        await worksheet.post_to_spreadsheet(name, distance,time)

def handle_result_updated(result):
    user_id = result.get('user_id')
    time = result.get('time')
    distance = result.get('distance')

    if user_id is not None and time is not None and distance is not None:
        user_name = next((u for u in users if u['userid'] == int(user_id)), None)['name']
        print(f"Result updated - Username: {user_name}, Time: {time}, Distance: {distance} meters")

def get_authorization_code():
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
        print()
    print(authorization_code)
    return authorization_code




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
