from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# This function asks the AI to find "hidden" words in the scramble
def analyze_text(text):
    prompt = f"""You are a 1939 Cryptanalyst. Look at this scrambled text: "{text}"
    1. Identify any 3-5 letter sequences that look like English or French words.
    2. Suggest 3 full words related to "Maps" or "Military" that might be hidden here.
    Return ONLY the words separated by commas. No sentences."""
    
    try:
        response = requests.post("http://localhost:11434/api/generate", 
            json={"model": "phi3", "prompt": prompt, "stream": False}, timeout=10)
        result = response.json().get('response', "")
        # Extract words (only A-Z)
        words = re.findall(r'[A-Z]{3,}', result.upper())
        return list(set(words))
    except:
        return []

@app.route('/get_cribs', methods=['POST'])
def get_cribs():
    data = request.json
    found = analyze_text(data.get("text", ""))
    return jsonify({"cribs": found})

if __name__ == '__main__':
    app.run(port=8080)
