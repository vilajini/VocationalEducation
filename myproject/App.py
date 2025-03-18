import openai
import nltk
import os
from nltk.tokenize import sent_tokenize
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
nltk.download('punkt')

#  API
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

# Store  questions
generated_questions = []


def preprocess_text(text, chunk_size=3):
    sentences = sent_tokenize(text)
    return [" ".join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]


#   input
textinput = '''
Repairing a laptop involves several steps, depending on the issue at hand. The first step is identifying the problem, which could be anything from hardware failure to software issues. For hardware issues, ensure the laptop is powered off and unplugged before proceeding.

Start by checking the battery if the laptop won't turn on. Sometimes, simply reseating the battery or replacing it can solve the issue. If the screen is blank, try connecting the laptop to an external monitor to determine if the issue is with the display or the internal components.

For software-related issues, booting the laptop in safe mode can help resolve conflicts or viruses. Running a virus scan and updating the operating system may also fix the problem.

If your laptop has a malfunctioning keyboard or trackpad, try removing any debris, cleaning the components, or updating drivers. In cases of overheating, cleaning out the fan or replacing thermal paste can prevent damage to the internal components.

If the laptop is slow, consider upgrading the RAM or replacing the hard drive with an SSD for better performance. Always make sure to back up data before performing repairs.

In severe cases, replacing faulty components like the motherboard or screen may be necessary. If you're unsure about any repair, it's best to consult a professional technician to avoid further damage.
'''


def generate_questions(textinput, difficulty):
    prompt = (f"Create at least 5 electrician study questions based on the following text:\n"
              f"{textinput}\n"
              f"The questions must be multiple-choice with 4 options. "
              f"Ensure that the questions are meaning-based and cover a variety of aspects from the text. "
              f"Generate at least 5 unique and distinct questions. "
              f"Make sure to adjust the difficulty to {difficulty} level.")

    # Call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=4096
    )

    response_text = response['choices'][0]['message']['content'].strip()
    lines = response_text.split("\n")

    question = lines[0].replace("Question: ", "").strip() if lines else ""
    options = [line.strip() for line in lines[1:5]] if len(lines) > 1 else []
    correct_answer = lines[-1].replace("Correct Answer: ", "").strip() if len(lines) > 1 else ""

    return {
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    }


# multiple questions.
def process_text_and_generate_questions(text, difficulty):
    global generated_questions
    generated_questions = []
    text_chunks = preprocess_text(text)

    for chunk in text_chunks:
        result = generate_questions(chunk, difficulty)
        if result["question"]:
            generated_questions.append(result)


# Define the difficulty 
difficulty_level = "Low level"
process_text_and_generate_questions(textinput, difficulty_level)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generate_questions', methods=['POST'])
def generate_questions_api():
    difficulty = request.json.get('difficulty')  
    process_text_and_generate_questions(textinput, difficulty)  
    return jsonify({"message": "Questions generated successfully"})



@app.route('/get_questions', methods=['GET'])
def get_questions():
    return jsonify({"questions": generated_questions})


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    data = request.json
    user_answers = data.get('answers', {})

    correct_count = 0
    results = []

    for idx, question in enumerate(generated_questions):
        correct_answer = question["correct_answer"]
        user_answer = user_answers.get(str(idx), "")
        result = "Correct" if user_answer == correct_answer else "Incorrect"

        if result == "Correct":
            correct_count += 1

        results.append({
            "question": question["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "result": result
        })

    total_questions = len(generated_questions)
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    return jsonify({
        "results": results,
        "correct_count": correct_count,
        "incorrect_count": total_questions - correct_count,
        "accuracy": accuracy
    })


@app.route('/chatbot', methods=['GET'])
def chatbot_ui():
    return render_template('chatbot.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message')
    selected_language = data.get('language')

    #  formatted prompt
    prompt = f"You are an assistant that helps people with electrician studies. Respond to the user's query in {selected_language}: {user_message}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        chatbot_message = response['choices'][0]['message']['content']
        return jsonify({"message": chatbot_message})

    except Exception as e:
        return jsonify({"message": "Sorry, there was an error processing your request."})


if __name__ == '__main__':
    app.run(debug=True)
