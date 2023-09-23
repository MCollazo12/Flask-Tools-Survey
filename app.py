from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

app.debug = True
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


SURVEY_QUESTIONS = len(satisfaction_survey.questions)


@app.route('/')
def show_survey():
    """Displays survey title and instructions on homepage"""
    title = satisfaction_survey.title
    inst = satisfaction_survey.instructions    
    return render_template('satisfaction_survey.html', title=title, inst=inst)

#Utilize post request to create a session for the user
@app.route('/set-session', methods=['POST'])
def handle_session():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:ques_number>')
def show_questions(ques_number):
    """Displays the current survey question to be answered"""
    responses = session['responses']
         
    #Handles user trying to skip questions     
    if len(responses) != ques_number:
        flash('Please answer this question before moving on', 'incorrect_ques')
        return redirect(f"/questions/{len(responses)}")
    
    #User has answered all questions -> Display thank you page
    if len(responses) == SURVEY_QUESTIONS:
        return redirect('/thank-you')
    
    survey_ques = satisfaction_survey.questions[ques_number]
    return render_template('questions.html', survey_ques=survey_ques, ques_number=ques_number)


@app.route('/answer', methods=['POST'])
def answer_page():
    """ Stores user answer in responses list and redirect to the next question """
    
    #Request the user's answer
    ans = request.form['choice']
    
    #Append thier answer to the session
    responses = session['responses']
    responses.append(ans)
    session['responses'] = responses
    
    #Check for completed survey else move on to the next question
    if len(responses) == SURVEY_QUESTIONS:
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/thank-you')
def thank_you_page():
    """Page to be shown once the user completes the survey"""
    return render_template('thank-you.html')


    