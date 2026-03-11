from flask import Blueprint
from app.controllers.deadline_controller import DeadlineController

deadline_bp = Blueprint('deadlines', __name__, url_prefix='/api/deadlines')


@deadline_bp.route('/student/<string:ma_sv>', methods=['GET'])
def get_deadlines_by_student(ma_sv):
    return DeadlineController.get_deadlines_by_student(ma_sv)

@deadline_bp.route('/student/<string:ma_sv>/upcoming', methods=['GET'])
def get_upcoming_deadlines(ma_sv):
    return DeadlineController.get_upcoming_deadlines(ma_sv)

@deadline_bp.route('/<string:ma_dl>', methods=['GET'])
def get_deadline(ma_dl):
    return DeadlineController.get_deadline(ma_dl)

@deadline_bp.route('/', methods=['POST'])
def create_deadline():
    return DeadlineController.create_deadline()

@deadline_bp.route('/<string:ma_dl>/complete', methods=['PUT'])
def mark_completed(ma_dl):
    """PUT /api/deadlines/<ma_dl>/complete - Đánh dấu hoàn thành"""
    return DeadlineController.mark_completed(ma_dl)

@deadline_bp.route('/<string:ma_dl>', methods=['PUT'])
def update_deadline(ma_dl):
    return DeadlineController.update_deadline(ma_dl)

@deadline_bp.route('/<string:ma_dl>', methods=['DELETE'])
def delete_deadline(ma_dl):
    return DeadlineController.delete_deadline(ma_dl)