from flask import Blueprint
from app.controllers.schedule_controller import ScheduleController

schedule_bp = Blueprint('schedules', __name__, url_prefix='/api/schedules')


@schedule_bp.route('/student/<string:ma_sv>', methods=['GET'])
def get_schedule_by_student(ma_sv):
    return ScheduleController.get_schedule_by_student(ma_sv)

@schedule_bp.route('/student/<string:ma_sv>/day/<int:thu>', methods=['GET'])
def get_schedule_by_day(ma_sv, thu):
    return ScheduleController.get_schedule_by_day(ma_sv, thu)

@schedule_bp.route('/<string:ma_lh>', methods=['GET'])
def get_schedule(ma_lh):
    return ScheduleController.get_schedule(ma_lh)

@schedule_bp.route('/', methods=['POST'])
def create_schedule():
    return ScheduleController.create_schedule()

@schedule_bp.route('/<string:ma_lh>', methods=['PUT'])
def update_schedule(ma_lh):
    return ScheduleController.update_schedule(ma_lh)

@schedule_bp.route('/<string:ma_lh>', methods=['DELETE'])
def delete_schedule(ma_lh):
    return ScheduleController.delete_schedule(ma_lh)