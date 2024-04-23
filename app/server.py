import os
from os.path import join, dirname
from flask import Flask, render_template, session, request, redirect, url_for
from Cipher import Cipher
from fileStorage import User, register_user, check_credentials
from fileStorage import update_password
from fileStorage import clear_user
import json
from functools import wraps

app = Flask(__name__, template_folder='/src/app/templates', static_folder='/src/app/static', static_url_path='')

app.config["SECRET_KEY"] ='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

cipher = Cipher()

user_data = {}

def testing(x):
    return x + 1

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home', methods=['GET'], endpoint='home')
@login_required
def home():
    return render_template('home.html')

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
        username = request.form['username']
        password = request.form['password']
        passkey = request.form['passkey']
        if register_user(username, password, passkey):
            return redirect(url_for('login'))
        else:
            error_message = "Username already exists"
            return render_template('register.html', error=error_message)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('username', None)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_valid, error_message = check_credentials(username, password)
        if is_valid:
            session['username'] = username
            user_data[username] = {'encrypted_text': '', 'encrypted_data_list': []}
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@app.route('/username', methods=['GET', 'POST'])
@login_required
def username():
    if request.method == 'POST':
        new_password = request.form['new_password']
        username = session.get('username')  
        update_password(username, new_password)
        session.pop('username', None)  
        return render_template('username.html')
    return render_template('username.html')

from flask import session

@app.route('/encryption', methods=['GET', 'POST'])
@login_required
def encryption():
    username = session.get('username')

    if username not in user_data:
        user_data[username] = {'encrypted_text': '', 'encrypted_data_list': []}

    base64_encoded_text = ""

    if request.method == 'POST':
        if 'encrypt' in request.form:
            password_text = request.form['password_text']
            encrypted_text = cipher.encrypt(password_text)
            base64_encoded_text = cipher.base64Encode(encrypted_text)
            user_data[username]['encrypted_text'] = encrypted_text
        elif 'save' in request.form:
            tag = request.form.get('tag', '')
            encrypted_text = user_data[username]['encrypted_text']
            if tag and encrypted_text:
                encrypted_data = {'tag': tag, 'encrypted_text': encrypted_text}
                user_data[username]['encrypted_data_list'].append(encrypted_data)
                user_data[username]['encrypted_text'] = ''

    encrypted_text = user_data[username]['encrypted_text']
    return render_template('encryption.html', encrypted_text=encrypted_text, base64_encoded_text=base64_encoded_text)

@app.route('/decryption', methods=['GET', 'POST'], endpoint='decryption')
@login_required
def decryption():
    if request.method == 'POST':
        encrypted_text = request.form['encrypted_text']
        decrypted_text = cipher.decrypt(encrypted_text)
        return render_template('decryption.html', decrypted_text=decrypted_text)
    return render_template('decryption.html')

@app.route('/list', methods=['GET'])
@login_required
def list():
    username = session.get('username')

    if username not in user_data:
        user_data[username] = {'encrypted_text': '', 'encrypted_data_list': []}

    encrypted_data_list = user_data[username].get('encrypted_data_list', [])
    if encrypted_data_list:
        return render_template('list.html', encrypted_data=encrypted_data_list)
    return render_template('list.html', message="No encrypted data available.")
    

@app.route('/clear_user', methods=['POST'])
def clear_user_route():
    if request.method == 'POST':
        username = request.form['username']
        clear_user(username)
        return 'User cleared successfully'
    else:
        return 'Invalid request method'

@app.route('/logout', methods=['GET'], endpoint='logout')
@login_required
def logout():
    username = session.get('username')
    session.pop('username', None)
    if username in user_data:
        try:
            user = User.get(User.username == username)
            user.encrypted_text = json.dumps(user_data[username]['encrypted_data_list'])
            user.save()
        except User.DoesNotExist:
            print(f"User '{username}' not found.")
        del user_data[username] 
    session.clear() 
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
