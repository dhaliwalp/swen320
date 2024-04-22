import os
from peewee import SqliteDatabase, Model, CharField

db = SqliteDatabase('users.db')

class User(Model):
    username = CharField(unique=True)
    password = CharField()
    passkey = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([User])

def register_user(username, password, passkey):
    User.create(username=username, password=password, passkey=passkey)

def check_credentials(username, password):
    try:
        user = User.get(User.username == username)
        return user.password == password
    except User.DoesNotExist:
        return False

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


