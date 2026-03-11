from flask import Blueprint
from app.controllers.subject_controller import SubjectController

# Tạo Blueprint
subject_bp = Blueprint('subjects', __name__, url_prefix='/api/subjects')

# Routes

@subject_bp.route('/', methods=['GET'])
def get_all_subjects():
    """GET /api/subjects - Lấy tất cả môn học"""
    return SubjectController.get_all_subjects()

@subject_bp.route('/student/<string:ma_sv>', methods=['GET'])
def get_subjects_by_student(ma_sv):
    """GET /api/subjects/student/<ma_sv> - Lấy môn học của sinh viên"""
    return SubjectController.get_subjects_by_student(ma_sv)

@subject_bp.route('/<string:ma_mh>', methods=['GET'])
def get_subject(ma_mh):
    """GET /api/subjects/<ma_mh> - Lấy một môn học"""
    return SubjectController.get_subject(ma_mh)

@subject_bp.route('/', methods=['POST'])
def create_subject():
    """POST /api/subjects - Tạo môn học mới"""
    return SubjectController.create_subject()

@subject_bp.route('/<string:ma_mh>', methods=['PUT'])
def update_subject(ma_mh):
    """PUT /api/subjects/<ma_mh> - Cập nhật môn học"""
    return SubjectController.update_subject(ma_mh)

@subject_bp.route('/<string:ma_mh>', methods=['DELETE'])
def delete_subject(ma_mh):
    """DELETE /api/subjects/<ma_mh> - Xóa môn học"""
    return SubjectController.delete_subject(ma_mh)