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
    { "question": "What is AI?", "answer": "AI, or Artificial Intelligence, refers to machines that can perform tasks that typically require human intelligence, such as learning, problem-solving, and decision-making." },
    { "question": "How does AI work?", "answer": "AI works by using algorithms and models to process data, learn patterns, and make predictions or decisions." },
    { "question": "What are the types of AI?", "answer": "The main types of AI are Narrow AI (task-specific), General AI (human-like intelligence), and Super AI (beyond human intelligence)." },
    { "question": "What is machine learning?", "answer": "Machine learning is a subset of AI that enables computers to learn from data and improve performance without being explicitly programmed." },
    { "question": "What is deep learning?", "answer": "Deep learning is a type of machine learning that uses neural networks with many layers to analyze complex data patterns." },
    { "question": "What is natural language processing?", "answer": "Natural Language Processing (NLP) is a branch of AI that enables machines to understand, interpret, and generate human language." },
    { "question": "How do AI chatbots work?", "answer": "AI chatbots use NLP and machine learning to process user input, understand intent, and generate relevant responses." },
    { "question": "Can AI think like a human?", "answer": "No, AI does not have consciousness or emotions; it simulates human-like behavior based on data and algorithms." },
    { "question": "What is the difference between AI and automation?", "answer": "Automation follows pre-defined rules, while AI learns from data and makes decisions dynamically." },
    { "question": "How is AI different from human intelligence?", "answer": "AI processes information faster but lacks human creativity, emotions, and common sense reasoning." },
    
    { "question": "What are some common applications of AI?", "answer": "AI is used in healthcare, finance, robotics, autonomous vehicles, customer service, and more." },
    { "question": "Can AI replace humans in jobs?", "answer": "AI can automate some tasks, but human creativity, critical thinking, and emotional intelligence remain irreplaceable." },
    { "question": "What is reinforcement learning?", "answer": "Reinforcement learning is an AI training method where agents learn by receiving rewards or penalties based on their actions." },
    { "question": "What is a neural network?", "answer": "A neural network is a set of algorithms modeled after the human brain to recognize patterns and make decisions." },
    { "question": "What is computer vision?", "answer": "Computer vision is a field of AI that enables machines to interpret and process visual data from the world." },
    { "question": "How does AI impact cybersecurity?", "answer": "AI helps detect threats, analyze risks, and automate responses to enhance cybersecurity." },
    { "question": "Can AI write code?", "answer": "Yes, AI-powered tools like GitHub Copilot can assist developers by generating code snippets." },
    { "question": "What is an AI model?", "answer": "An AI model is a mathematical representation trained on data to make predictions or decisions." },
    { "question": "How do AI algorithms work?", "answer": "AI algorithms process data, find patterns, and make decisions based on statistical and logical techniques." },
    { "question": "What is an AI bias?", "answer": "AI bias occurs when an AI system produces unfair or prejudiced outcomes due to biased training data." },
    
    { "question": "What is GPT?", "answer": "GPT (Generative Pre-trained Transformer) is an AI model developed by OpenAI for natural language understanding and generation." },
    { "question": "How does ChatGPT work?", "answer": "ChatGPT uses deep learning to generate human-like responses based on input text." },
    { "question": "What is OpenAI?", "answer": "OpenAI is an AI research organization that develops AI technologies, including ChatGPT and DALL·E." },
    { "question": "Can AI create images?", "answer": "Yes, AI models like DALL·E can generate images based on text descriptions." },
    { "question": "What is an AI chatbot?", "answer": "An AI chatbot is a software program that simulates human conversation using NLP and machine learning." },
    { "question": "Can AI understand emotions?", "answer": "AI can analyze sentiment in text and voice but does not truly feel emotions." },
    { "question": "What is the Turing Test?", "answer": "The Turing Test evaluates whether a machine can exhibit human-like intelligence in conversation." },
    { "question": "How does AI impact the environment?", "answer": "AI requires significant computing power, which can contribute to energy consumption and carbon emissions." },
    { "question": "What is AGI?", "answer": "Artificial General Intelligence (AGI) refers to AI with human-like reasoning and adaptability." },
    { "question": "What is ASI?", "answer": "Artificial Super Intelligence (ASI) is a theoretical AI that surpasses human intelligence in all aspects." },
    { "question": "Can AI be dangerous?", "answer": "AI can pose risks if misused, including privacy violations, bias, and job displacement." },
    
    { "question": "What is the future of AI?", "answer": "AI is expected to advance in automation, healthcare, robotics, and creative industries." },
    { "question": "How does AI learn?", "answer": "AI learns through training data, algorithms, and models that adjust over time." },
    { "question": "What is an AI assistant?", "answer": "An AI assistant, like Siri or Alexa, helps users with tasks using voice or text commands." },
    { "question": "What is edge AI?", "answer": "Edge AI processes data locally on a device rather than relying on cloud computing." },
    { "question": "How is AI used in gaming?", "answer": "AI enhances game design, NPC behavior, and adaptive difficulty in video games." },
    { "question": "What is ethical AI?", "answer": "Ethical AI focuses on fairness, transparency, and reducing bias in AI systems." },
    { "question": "Can AI develop creativity?", "answer": "AI can generate art, music, and writing, but it lacks true human creativity." },
    { "question": "What is federated learning?", "answer": "Federated learning is a decentralized AI training approach that keeps data local and improves privacy." },
    { "question": "How does AI affect privacy?", "answer": "AI raises privacy concerns when collecting, storing, and analyzing user data." },
    { "question": "Can AI predict the future?", "answer": "AI can make data-driven predictions but cannot foresee random events." },
    { "question": "Who designed AI-Bot?", "answer": "AI-Bot was designed by Pradeep Yadav." },
    { "question": "What is your name?", "answer": "AI-Bot ." },
    { "question": "Who is the owner of AI-Bot?", "answer": "Pradeep Yadav is the owner of AI-Bot." },
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
