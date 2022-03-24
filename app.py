from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []



@app.get("/")
def show_start():
    """Shows survey start page"""

    return render_template("survey_start.html", title = survey.title, instructions = survey.instructions, q_id=0)

@app.get("/questions/<int:q_id>")
def show_question(q_id):
    """Shows questions"""

    curr_question = survey.questions[q_id]

    return render_template("question.html", question = curr_question)

# @app.VERB(f"/questions/{curr_question}")


@app.post("/answer")
def log_answer():
    """logs answer in responses list and redirects to next"""

    value = request.form.get("answer")
    responses.append(value)


    if len(responses) == len(survey.questions):
        return redirect("/completion")

    return redirect(f"/questions/{len(responses)}")


@app.get("/completion")
def say_thanks():
    """says thank you for completing survey"""

    return render_template("completion.html")