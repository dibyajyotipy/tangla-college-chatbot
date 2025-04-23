from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer, util
import sqlite3

app = Flask(__name__, template_folder='HTML', static_folder='CSS')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

# Load Q&A from SQLite database
def load_qa_data():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM qa")
    data = cursor.fetchall()
    conn.close()
    return dict(data)

# Load data from DB
qa_data = load_qa_data()
questions = list(qa_data.keys())

# Load model and encode questions
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
question_embeddings = model.encode(questions, convert_to_tensor=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-answer', methods=['POST'])
def get_answer():
    user_input = request.json['message']
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    similarity = util.cos_sim(user_embedding, question_embeddings)[0]
    best_match_idx = similarity.argmax().item()
    score = similarity[best_match_idx].item()

    if score > 0.6:
        matched_question = questions[best_match_idx]
        answer = qa_data[matched_question]
    else:
        answer = "Sorry, Iam Still Learning!"

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
