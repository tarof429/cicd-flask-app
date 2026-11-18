from werkzeug.security import generate_password_hash

def test_pasword_length():
    password = generate_password_hash('verysecret')
    assert len(password) <= 255

    password = generate_password_hash('admin')
    assert len(password) <= 255