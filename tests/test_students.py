import pytest
from app import app, db, Student

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_healthcheck(client):
    response = client.get('/api/v1/healthcheck')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_create_student(client):
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 20,
        'grade': 'A'
    }
    response = client.post('/api/v1/students', json=student_data)
    assert response.status_code == 201
    assert 'id' in response.json

def test_get_student(client):
    # First create a student
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    create_response = client.post('/api/v1/students', json=student_data)
    student_id = create_response.json['id']

    # Then get the student
    response = client.get(f'/api/v1/students/{student_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'

def test_update_student(client):
    # Create student
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    create_response = client.post('/api/v1/students', json=student_data)
    student_id = create_response.json['id']

    # Update student
    update_data = {'name': 'John Smith'}
    response = client.put(f'/api/v1/students/{student_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['name'] == 'John Smith'

def test_delete_student(client):
    # Create student
    student_data = {
        'name': 'John Doe',
        'email': 'john@example.com'
    }
    create_response = client.post('/api/v1/students', json=student_data)
    student_id = create_response.json['id']

    # Delete student
    response = client.delete(f'/api/v1/students/{student_id}')
    assert response.status_code == 200

    # Verify student is deleted
    get_response = client.get(f'/api/v1/students/{student_id}')
    assert get_response.status_code == 403
