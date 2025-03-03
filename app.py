from flask import Flask, request, jsonify
from flask_cors import CORS
import difflib  # For fuzzy matching

app = Flask(__name__)
CORS(app)  # Enable CORS

# Sample dataset
dataset = [
    {"question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines."},
    {"question": "Who is the Prime Minister of India?", "answer": "The Prime Minister of India is Narendra Modi (as of 2024)."},
    {"question": "What is Python?", "answer": "Python is a high-level programming language used for various applications."},
    {"question": "What is the capital of France?", "answer": "The capital of France is Paris."},
    {"question": "Who discovered gravity?", "answer": "Gravity was discovered by Sir Isaac Newton."},
    {"question": "What is the speed of light?", "answer": "The speed of light is approximately 299,792,458 meters per second."},
    {"question": "What is blockchain?", "answer": "Blockchain is a decentralized digital ledger that records transactions securely."},
    {"question": "What is IoT?", "answer": "IoT (Internet of Things) refers to interconnected devices communicating over the internet."},
    {"question": "Who invented the telephone?", "answer": "The telephone was invented by Alexander Graham Bell."},
    {"question": "What is quantum computing?", "answer": "Quantum computing uses quantum mechanics principles to perform calculations."},
    {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that enables systems to learn from data."},
    {"question": "What is deep learning?", "answer": "Deep learning is a subset of ML using neural networks to model complex patterns."},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter is the largest planet in our solar system."},
    {"question": "What is photosynthesis?", "answer": "Photosynthesis is the process by which plants convert sunlight into energy."},
    {"question": "Who wrote Hamlet?", "answer": "Hamlet was written by William Shakespeare."},
    {"question": "What is the boiling point of water?", "answer": "Water boils at 100°C (212°F) at sea level."},
    {"question": "What is the chemical formula for water?", "answer": "The chemical formula for water is H2O."},
    {"question": "What is the human body's largest organ?", "answer": "The skin is the largest organ of the human body."},
    {"question": "What is the powerhouse of the cell?", "answer": "The mitochondrion is known as the powerhouse of the cell."},
    {"question": "Who painted the Mona Lisa?", "answer": "The Mona Lisa was painted by Leonardo da Vinci."}
]

def find_best_match(user_input):
    """Finds the best answer from the dataset based on exact and fuzzy matches."""
    user_input_lower = user_input.lower().strip()

    # Step 1: Check for exact match
    for entry in dataset:
        if entry["question"].lower() == user_input_lower:
            return entry["answer"]

    # Step 2: Check for keyword match
    matched_answers = []
    for entry in dataset:
        question_words = set(entry["question"].lower().split())
        input_words = set(user_input_lower.split())

        if question_words & input_words:  # Common words found
            matched_answers.append(entry["answer"])

    if len(matched_answers) == 1:
        return matched_answers[0]
    elif len(matched_answers) > 1:
        return "🤖 Your question is not clear. Please provide more details."

    # Step 3: Use fuzzy matching if no keyword match
    questions = [entry["question"] for entry in dataset]
    best_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    if best_match:
        for entry in dataset:
            if entry["question"] == best_match[0]:
                return entry["answer"]

    # Step 4: Single-word queries handling
    for entry in dataset:
        if user_input_lower in entry["question"].lower():
            return entry["answer"]

    return "🤖 Sorry, I don't have an answer for that."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data.get("question", "")
    answer = find_best_match(user_question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
