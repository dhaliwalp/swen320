import os
from os.path import join, dirname
from flask import Flask, render_template, session, request, redirect, url_for
# from Cipher.py import Cipher

app = Flask(__name__, template_folder='/src/app/templates', static_folder='/src/app/static', static_url_path='')

app.config["SECRET_KEY"] ='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

# cipher = Cipher()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    control_val = 0
    if request.method == 'POST':
        if 'cval' in request.form:
            control_val = request.form['cval']
    else:
        if 'cval' in request.args:
            control_val = request.args.get('cval')
    my_name = "Tester ABC"
    my_var1_val = "This is a good test!!"
    return render_template('home.html', username=my_name, my_var1=my_var1_val, is_show=control_val)

@app.route('/post_form')
def get_post_form():
    return render_template('post_form.html')


@app.route('/post_submit', methods=['POST'])
def form_response_ex():
    user = ""
    if request.method == 'POST':
        if 'field_a' in request.form:
            field_a_val = request.form['field_a']
        if 'number' in request.form:
            number = request.form['number']
        if 'field_b' in request.form:
            field_b_val = request.form['field_b']
            session['field_b'] = field_b_val
        return render_template('response.html', field_a=field_a_val, number=number)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            if len(username) > 10 or len(username) < 5:
                return render_template('register.html', error="Username length needs to be between 5 and 10 characters")
        if 'password' in request.form:
            password = request.form['password']
            if len(password) > 20 or len(password) < 8:
                return render_template('register.html', error="Password length needs to be between 8 and 20 characters")
        if 'passkey' in request.form:
            passkey = request.form['passkey']
            if len(passkey) > 30 or len(passkey) < 10:
                return render_template('register.html', error="Passkey length needs to be between 10 and 30 characters")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'username' in request.form:
            username = request.form['username']
            if len(username) > 10 or len(username) < 5:
                return render_template('login.html', error="Username length needs to be between 5 and 10 characters")
        if 'password' in request.form:
            password = request.form['password']
            if len(password) > 20 or len(password) < 8:
                return render_template('login.html', error="Password length needs to be between 8 and 20 characters")
        return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
