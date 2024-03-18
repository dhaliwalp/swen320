import pytest
from app.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
# white-box testing
def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home Page' in response.data

# white-box testing
def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

# white-box testing
def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# white-box testing
def test_post_form(client):
    response = client.get('/post_form')
    assert response.status_code == 200
    assert b'Post Form' in response.data

# white-box testing
def test_post_submit(client):
    response = client.get('/post_submit')
    assert response.status_code == 405

# white-box testing
def test_form_response_ex(client):
    response = client.get('/form_response_ex')
    assert response.status_code == 405

# white-box testing
def test_register_post(client):
    response = client.post('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

# white-box testing
def test_login_post(client):
    response = client.post('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

# black-box testing
def test_register_post_with_data(client):
    response = client.post('/register', data=dict(username='test', password='test', passkey='test'))
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/login'

# black-box testing
def test_login_post_with_data(client):
    response = client.post('/login', data=dict(username='test', password='test'))
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/home'

# black-box testing
def test_register_post_with_invalid_data(client):
    response = client.post('/register', data=dict(username='test', password='test', passkey='mymomdoesntlikeitwhenimnaughty'))
    assert response.status_code == 200
    assert b'Passkey length needs to be between 10 and 30 characters' in response.data

# black-box testing
def test_login_post_with_invalid_data(client):
    response = client.post('/login', data=dict(username='test', password='somethingthatpeoplethinkisoingtobesafebutactuallyisntsafeatall'))
    assert response.status_code == 200
    assert b'Password length needs to be between 8 and 20 characters' in response.data

# black-box testing
def test_post_submit_with_data(client):
    response = client.post('/post_submit', data=dict(field_a='test', number='123', field_b='test'))
    assert response.status_code == 200
    assert b'test' in response.data
    assert b'123' in response.data
    assert b'test' in response.data