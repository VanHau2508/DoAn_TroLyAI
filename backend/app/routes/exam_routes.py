from flask import Blueprint
from app.controllers.exam_controller import ExamController

exam_bp = Blueprint('exams', __name__, url_prefix='/api/exams')


@exam_bp.route('/student/<string:ma_sv>', methods=['GET'])
def get_exams_by_student(ma_sv):
    return ExamController.get_exams_by_student(ma_sv)

@exam_bp.route('/student/<string:ma_sv>/upcoming', methods=['GET'])
def get_upcoming_exams(ma_sv):
    return ExamController.get_upcoming_exams(ma_sv)

@exam_bp.route('/<string:ma_lt>', methods=['GET'])
def get_exam(ma_lt):
    return ExamController.get_exam(ma_lt)

@exam_bp.route('/', methods=['POST'])
def create_exam():
    return ExamController.create_exam()

@exam_bp.route('/<string:ma_lt>', methods=['PUT'])
def update_exam(ma_lt):
    return ExamController.update_exam(ma_lt)

@exam_bp.route('/<string:ma_lt>', methods=['DELETE'])
def delete_exam(ma_lt):
    return ExamController.delete_exam(ma_lt)