from flask import Flask,render_template
from flask import request
# from forms import RegistrationForm,LoginForm

app = Flask(__name__)

@app.route('/')
def response():
    # form = RegistrationForm()
    return render_template('index.html')

@app.route('/form',methods=["POST"])
def form():
    allow = request.form['choice']
    print(allow)
    f = open('response.txt','w')
    f.write(allow)
    f.close()
    return render_template('form.html')