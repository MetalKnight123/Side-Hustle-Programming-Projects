from flask import Flask, render_template, request
from chatbot6 import Chatbot

app = Flask(__name__)
bot = Chatbot()  # Create one chatbot instance

@app.route("/", methods=["GET", "POST"])
def index():
    user_input = ""
    ai_response = ""

    if request.method == "POST":
        user_input = request.form["message"]
        ai_response = bot.generate_response(user_input)

    return render_template("index.html", user_input=user_input, ai_response=ai_response)

if __name__ == "__main__":
    app.run(debug=True)
