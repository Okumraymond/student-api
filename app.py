from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    grade = db.Column(db.String(10))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'grade': self.grade
        }

# Health Check Endpoint
@app.route('/api/v1/healthcheck', methods=['GET'])
def healthcheck():
    logger.info('Health check requested')
    return jsonify({'status': 'healthy'}), 200

# Student CRUD Endpoints
@app.route('/api/v1/students', methods=['POST'])
def create_student():
    data = request.get_json()
    logger.info(f'Creating student with data: {data}')
    
    if not data or not all(key in data for key in ['name', 'email']):
        logger.error('Invalid student data provided')
        return jsonify({'error': 'Name and email are required'}), 400
    
    student = Student(
        name=data['name'],
        email=data['email'],
        age=data.get('age'),
        grade=data.get('grade')
    )
    
    try:
        db.session.add(student)
        db.session.commit()
        logger.info(f'Student created with ID: {student.id}')
        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating student: {str(e)}')
        return jsonify({'error': 'Could not create student'}), 500

@app.route('/api/v1/students', methods=['GET'])
def get_all_students():
    logger.info('Fetching all students')
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200

@app.route('/api/v1/students/<int:id>', methods=['GET'])
def get_student(id):
    logger.info(f'Fetching student with ID: {id}')
    student = Student.query.get(id)
    if not student:
        logger.error(f'Student with ID {id} not found')
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict()), 200

@app.route('/api/v1/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        logger.error(f'Student with ID {id} not found for update')
        return jsonify({'error': 'Student not found'}), 404
    
    data = request.get_json()
    logger.info(f'Updating student ID {id} with data: {data}')
    
    if 'name' in data:
        student.name = data['name']
    if 'email' in data:
        student.email = data['email']
    if 'age' in data:
        student.age = data['age']
    if 'grade' in data:
        student.grade = data['grade']
    
    try:
        db.session.commit()
        logger.info(f'Student with ID {id} updated successfully')
        return jsonify(student.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating student ID {id}: {str(e)}')
        return jsonify({'error': 'Could not update student'}), 500

@app.route('/api/v1/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        logger.error(f'Student with ID {id} not found for deletion')
        return jsonify({'error': 'Student not found'}), 404
    
    try:
        db.session.delete(student)
        db.session.commit()
        logger.info(f'Student with ID {id} deleted successfully')
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting student ID {id}: {str(e)}')
        return jsonify({'error': 'Could not delete student'}), 500

if __name__ == '__main__':
    app.run(debug=True)
