from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []
SURVEY_QUESTIONS = len(satisfaction_survey.questions)


@app.route('/')
def show_survey():
    """Displays survey title and instructions on homepage"""
    title = satisfaction_survey.title
    inst = satisfaction_survey.instructions    
    return render_template('satisfaction_survey.html', title=title, inst=inst)

@app.route('/questions/<int:ques_number>')
def show_questions(ques_number):
    """Handles"""
         
    if ques_number > len(responses) or ques_number > len(satisfaction_survey.questions):
        flash('Please answer this question before moving on', 'incorrect_ques')
        return redirect(f'/questions/{len(responses)}')
    
    if len(responses) == SURVEY_QUESTIONS:
        return redirect('/thank-you')
    
    survey_ques = satisfaction_survey.questions[ques_number]

    return render_template('questions.html', survey_ques=survey_ques, ques_number=ques_number)


@app.route('/answer', methods=['POST'])
def answer_page():
    """ Stores user answer in responses list and redirects to next question """
    ans = request.form.get('choice')
    responses.append(ans)
    
    ques_num = int(request.form.get('ques_number'))
    return redirect(f'/questions/{ques_num + 1}')


@app.route('/thank-you')
def thank_you_page():
    return render_template('thank-you.html', responses=responses)


    