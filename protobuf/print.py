
# Updated code to use the new JWT API as requested
# New API: https://mafuuu-token-converter.onrender.com/access-jwt?uid=UID&password=PASS

import sys
sys.path.append("/")

from flask import Flask, jsonify, request, make_response
import requests
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

app = Flask(__name__)

def get_jwt_from_new_api(uid, password):
    """
    Fetch JWT from the new API provided by the user.
    """
    url = f"https://mafuuu-token-converter.onrender.com/access-jwt?uid={uid}&password={password}"
    
    try:
        response = requests.get(url, verify=False, timeout=20)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}", "raw": response.text}
    except Exception as e:
        return {"error": str(e)}

@app.route('/token', methods=['GET'])
def get_token_response():
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({"error": "Missing parameters: uid and password are required"}), 400

    result = get_jwt_from_new_api(uid, password)

    if "error" in result:
        return jsonify(result), 500

    # The new API seems to return the data directly
    return jsonify(result)

@app.route('/jwt', methods=['GET'])
def get_jwt_from_access():
    """
    Kept for backward compatibility but redirecting to the same logic if possible, 
    though the new API requires uid/password.
    """
    return jsonify({"error": "This endpoint now requires uid and password. Use /token?uid=UID&password=PASS"}), 400

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Free Fire Token Service (Updated)",
        "endpoints": {
            "/token?uid=&password=": "Get JWT token via new API",
        },
        "status": "running",
        "api_source": "https://mafuuu-token-converter.onrender.com"
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
