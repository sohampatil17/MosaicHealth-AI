from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Enable CORS

# Set your OpenAI API key here

@app.route('/process_transcript', methods=['POST'])
def process_transcript():
    data = request.json
    print(request.json)
    transcript = data.get('transcript', '')  # Extract the transcript from the incoming request

    # Define the system and user messages for OpenAI
    messages = [
        {
            "role": "system",
            "content": """You are a helpful medical data assistant. Your job is to understand the doctor-patient interaction and create a SOAP formatted formal and succinct summary of the interaction, incorporating the important data mentioned in the transcript.
            """
        },
        {
            "role": "user",
            "content": transcript  # The transcript received from the client
        }
    ]

    # Call OpenAI's API
    response = client.chat.completions.create(model="gpt-4-0125-preview",
    messages=messages,
    max_tokens=1000)

    # Extract the response content
    response_content = response.choices[0].message.content

    # Return the response content as JSON
    return jsonify({"result": response_content})

if __name__ == '__main__':
    app.run(debug=True)
