from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"


@app.get("/")
def show_start():
    """Shows survey start page"""
    session[RESPONSES_KEY] = []
    session["survey_complete"] = False

    return render_template(
        "survey_start.html", 
        title = survey.title,
        instructions = survey.instructions, 
        q_id=0
        )

@app.get("/questions/<int:q_id>")
def show_question(q_id):
    """Shows questions and checks if survey is completed"""
    if session["survey_complete"] == True:
        return redirect("/completion")
    elif session["survey_complete"] == False and len(session[RESPONSES_KEY]) == q_id:
        curr_question = survey.questions[len(session[RESPONSES_KEY])]
        return render_template("question.html", question = curr_question)
    else:
        flash('STOP TRYING TO ACCESS QUESTIONS OUT OF ORDER!')
        return redirect(f"/questions/{len(session[RESPONSES_KEY])}")


# @app.VERB(f"/questions/{curr_question}")


@app.post("/answer")
def log_answer():
    """Logs answer in responses list and redirects to next"""

    value = request.form.get("answer")
    answers = session[RESPONSES_KEY]
    answers.append(value)
    session[RESPONSES_KEY] = answers


    if len(answers) != len(survey.questions):
        return redirect(f"/questions/{len(answers)}")
    else:
        session["survey_complete"] = True
        return redirect("/completion")


@app.get("/completion")
def say_thanks():
    """Says thank you for completing survey"""

    return render_template("completion.html")