from flask import Blueprint
from app.controllers.student_controller import StudentController

# Tạo Blueprint
student_bp = Blueprint('students', __name__, url_prefix='/api/students')


# Routes
@student_bp.route('/', methods=['GET'])
def get_all_students():
    return StudentController.get_all_students()

@student_bp.route('/<string:ma_sv>', methods=['GET'])
def get_student(ma_sv):
    return StudentController.get_student(ma_sv)

@student_bp.route('/', methods=['POST'])
def create_student():
    return StudentController.create_student()

@student_bp.route('/<string:ma_sv>', methods=['PUT'])
def update_student(ma_sv):
    return StudentController.update_student(ma_sv)

@student_bp.route('/<string:ma_sv>', methods=['DELETE'])
def delete_student(ma_sv):
    return StudentController.delete_student(ma_sv)

@student_bp.route('/login', methods=['POST'])
def login():
    return StudentController.login()