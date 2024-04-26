from flask import Flask, render_template, request, jsonify
import re
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_answers', methods=['POST'])
def fetch_answers():
    url = request.form['url']
    copy_answers = request.form.get('copy_answers', False)

    activity_id = extract_activity_id(url)
    if activity_id is None:
        return jsonify({'error': 'Invalid URL format'})

    full_url = get_full_url_from_file(activity_id)
    if full_url:
        output = fetch_correct_answers(full_url)
        if output:
            if copy_answers:
                answers = "\n".join(output)
                return jsonify({'answers': answers})
            else:
                return jsonify({'answers': output})
        else:
            return jsonify({'error': 'No result found'})
    else:
        return jsonify({'error': 'Result not found in file'})

def extract_activity_id(url):
    match = re.search(r'/activity/([^/]+)/exercise', url)
    if match:
        return match.group(1)
    return None

def get_full_url_from_file(activity_id):
    try:
        with open('final_correct_response.txt', 'r') as file:
            for line in file:
                if activity_id in line:
                    return line.strip()
    except FileNotFoundError:
        return None
    return None

def fetch_correct_answers(full_url):
    headers = {
        'Host': 'app.ofppt-langues.ma',
        'X-Device-Uuid': 'c4369295-36a2-4d7b-bd6f-d805f76a5a60',
        'X-Altissia-Token': '1c9b5e0c51828d85bedbf26b940ffa7bdc5aa8c0407002c234e6c23ccd8087fc',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        content = response.json()
        if 'content' in content and 'items' in content['content'] and content['content']['items']:
            correct_answers_list = []
            if 'content' in content and 'items' in content['content']:
                for item in content['content']['items']:
                    correct_answers = item.get('correctAnswers')
                    if correct_answers:
                        correct_answers_list.extend(correct_answers)
            flattened_correct_answers = [answer for sublist in correct_answers_list for answer in sublist]
            return flattened_correct_answers
    except requests.RequestException as e:
        return None
    return None

if __name__ == "__main__":
    app.run(debug=True)
