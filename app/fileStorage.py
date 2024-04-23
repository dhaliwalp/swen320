import os
from peewee import SqliteDatabase, Model, CharField, TextField, ForeignKeyField

db = SqliteDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    passkey = CharField()

    class Meta:
        database = db

class EncryptedData(Model):
    user = ForeignKeyField(User, backref='encrypted_data')
    tag = CharField()
    encrypted_text = TextField()

    class Meta:
        database = db

db.connect()
db.create_tables([User, EncryptedData], safe=True)

def register_user(username, password, passkey):
    try:
        User.get(User.username == username)
        return False
    except User.DoesNotExist:
        User.create(username=username, password=password, passkey=passkey)
        return True

def check_credentials(username, password):
    if not username or not password:
        return False, None
    try:
        user = User.get(User.username == username)
        if user.password == password:
            return True, None
        else:
            return False, "Wrong password"
    except User.DoesNotExist:
        return False, "Wrong username"

def update_password(username, new_password):
    try:
        user = User.get(User.username == username)
        user.password = new_password
        user.save()
    except User.DoesNotExist:
        print(f"User '{username}' not found.")

def clear_user(username):
    try:
        user = User.get(User.username == username)
        user.delete_instance()
    except User.DoesNotExist:
        print(f"User '{username}' not found.")

def save_encrypted_data(username, tag, encrypted_text):
    try:
        user = User.get(User.username == username)
        EncryptedData.create(user=user, tag=tag, encrypted_text=encrypted_text)
    except User.DoesNotExist:
        print(f"User '{username}' not found.")

def get_encrypted_data(username):
    try:
        user = User.get(User.username == username)
        encrypted_data = list(user.encrypted_data)
        return encrypted_data
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
        return []

def delete_encrypted_data(username, data_id):
    try:
        user = User.get(User.username == username)
        encrypted_data = EncryptedData.get(EncryptedData.id == data_id, EncryptedData.user == user)
        encrypted_data.delete_instance()
    except (User.DoesNotExist, EncryptedData.DoesNotExist):
        print(f"User '{username}' or data with ID {data_id} not found.")