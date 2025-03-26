from flask import Flask, render_template, request, jsonify
import requests
import os
import random

app = Flask(__name__)

# DeepSeek API Configuration (stored server-side)
API_KEY = "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"
API_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# Data Preprocessing
def preprocess_input(raw_input):
    """Extract key product details from unstructured input."""
    if not raw_input.strip():
        return None
    return raw_input.strip()

# DeepSeek API Interaction
def generate_script(product_details, length):
    """Generate script using DeepSeek API based on desired length with rotating styles."""
    word_counts = {"short": 120, "medium": 250, "long": 500}
    
    # Rotating prompt variations for each length
    short_prompts = [
        f"Write a short, punchy TikTok-style UGC ad script (~{word_counts['short']} words) that grabs attention, uses casual Gen Z slang, and ends with a strong call-to-action. No visual or voice-over advice. Based on: {product_details}",
        f"Create a snappy, relatable UGC ad script (~{word_counts['short']} words) for TikTok, with a bold hook and chill vibe, pushing the product naturally. No visual or voice-over notes. Based on: {product_details}",
        f"Generate a quick, hype TikTok UGC script (~{word_counts['short']} words) that’s all vibes, no fluff, with a dope call-to-action. No visual or voice-over stuff. Based on: {product_details}"
    ]
    
    medium_prompts = [
        f"Write a casual, engaging UGC ad script (~{word_counts['medium']} words) blending a TikTok hook with some personal flair, keeping it real and ending with a call-to-action. No visual or voice-over advice. Based on: {product_details}",
        f"Create a chill, relatable UGC script (~{word_counts['medium']} words) that feels like a friend hyping the product, with a solid hook and natural push. No visual or voice-over notes. Based on: {product_details}",
        f"Generate a fun, medium-length UGC ad script (~{word_counts['medium']} words) with a catchy start and authentic vibe, wrapping up with a call-to-action. No visual or voice-over stuff. Based on: {product_details}"
    ]
    
    long_prompts = [
        f"Write a detailed, personal UGC ad script (~{word_counts['long']} words) like someone sharing their real experience with the product, keeping it natural and engaging, ending with a call-to-action. No visual or voice-over advice. Based on: {product_details}",
        f"Create a long, storytelling UGC script (~{word_counts['long']} words) where someone raves about their product journey, making it relatable and hype, with a call-to-action. No visual or voice-over notes. Based on: {product_details}",
        f"Generate an in-depth UGC ad script (~{word_counts['long']} words) that’s all about the user’s honest take on the product, full of personality and a strong close. No visual or voice-over stuff. Based on: {product_details}"
    ]
    
    # Pick a random prompt based on length
    if length == "short":
        prompt = random.choice(short_prompts)
    elif length == "medium":
        prompt = random.choice(medium_prompts)
    else:  # long
        prompt = random.choice(long_prompts)
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": word_counts[length] * 2
    }
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error generating script: {str(e)}"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/generate', methods=['POST'])
def generate_scripts():
    product_details = request.json.get('details')
    script_size = request.json.get('size')  # Get the selected size
    processed_input = preprocess_input(product_details)
    
    if not processed_input or not script_size:
        return jsonify({"error": "Please provide product details and select a script size"}), 400
    
    script = generate_script(processed_input, script_size)
    return jsonify({script_size: script})  # Return only the selected script

@app.route('/feedback', methods=['POST'])
def save_feedback():
    rating = request.json.get('rating')
    script_type = request.json.get('script_type')
    with open('feedback.txt', 'a') as f:
        f.write(f"{script_type}: {rating}\n")
    return jsonify({"message": "Feedback saved"}), 200

import os
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)