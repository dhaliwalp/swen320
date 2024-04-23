import os
from peewee import SqliteDatabase, Model, CharField, TextField

db = SqliteDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    passkey = CharField()
    encrypted_text = TextField(null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([User], safe=True)

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


