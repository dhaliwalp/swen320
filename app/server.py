import os
from os.path import join, dirname
from flask import Flask, render_template, session, request, redirect, url_for
from Cipher import Cipher
from fileStorage import register_user, check_credentials
from fileStorage import update_password
from fileStorage import clear_user
import json

app = Flask(__name__, template_folder='/src/app/templates', static_folder='/src/app/static', static_url_path='')

app.config["SECRET_KEY"] ='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

cipher = Cipher()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home', methods=['GET'], endpoint='home')
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
        register_user(username, password, passkey)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    session.pop('username', None)  
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('home'))  
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/username', methods=['GET', 'POST'])
def username():
    if request.method == 'POST':
        new_password = request.form['new_password']
        username = session.get('username')  
        update_password(username, new_password)
        session.pop('username', None)  
        return render_template('username.html')
    return render_template('username.html')

@app.route('/encryption', methods=['GET', 'POST'])
def encryption():
    if request.method == 'POST':
        password_text = request.form['password_text']
        encrypted_text = cipher.encrypt(password_text)
        session['encrypted_text'] = encrypted_text
        return render_template('encryption.html', encrypted_text=encrypted_text)
    return render_template('encryption.html')

@app.route('/decryption', methods=['GET', 'POST'], endpoint='decryption')
def decryption():
    if request.method == 'POST':
        encrypted_text = request.form['encrypted_text']
        decrypted_text = cipher.decrypt(encrypted_text)
        return render_template('decryption.html', decrypted_text=decrypted_text)
    return render_template('decryption.html')

@app.route('/list_array', methods=['GET', 'POST'])
def list_array():
    if request.method == 'POST':
        tag = request.form['tag']
        encrypted_text = session.get("encrypted_text")
        if encrypted_text:
            encrypted_data = {'tag': tag, 'encrypted_text': encrypted_text}
            session['encrypted_data'] = json.dumps(encrypted_data)
    return redirect(url_for('encryption'))

@app.route('/list', methods=['GET'])
def list():
    encrypted_data_json = session.get('encrypted_data')
    if encrypted_data_json:
        encrypted_data = json.loads(encrypted_data_json)
        return render_template('list.html', encrypted_data=encrypted_data)
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
def home():
    session.pop('username', None)  
    session.pop('encrypted_data', None)
    session.pop('tag', None)
    session.pop('encrypted_text', None)  
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
