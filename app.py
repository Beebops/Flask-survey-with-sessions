from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = 'responses'

@app.route('/')
def show_survey():
    """Starts the survey"""
    return render_template('survey-start.html', survey=survey)

@app.route('/start', methods=['POST'])
def start_questions():
    """Clear all responses from the session and start questions"""
    session[RESPONSES] = []
    return redirect('/question/0')

@app.route('/answer', methods=['POST'])
def handle_question():
    """Save the response and redirect to next question"""
    choice = request.form['answer']

    answers = session[RESPONSES]
    answers.append(choice)
    session[RESPONSES] = answers

    if len(answers) == len(survey.questions):
        return redirect('/finished')
    else:
        return redirect(f"/question/{len(answers)}")


@app.route('/question/<int:question_num>')
def show_question(question_num):
    """Show the current question"""
    answers = session.get(RESPONSES)

    if (answers is None):
        return redirect('/')

    if (len(answers) == len(survey.questions)):
        return redirect('/finished')
    
    if (len(answers) != question_num):
        flash(f"Invalid question number: {question_num}")
        return redirect(f"/question/{len(answers)}")

    question = survey.questions[question_num]
    return render_template('question.html', question=question, question_num=question_num)

@app.route('/finished')
def finished_survey():
    return render_template('finished.html')