from flask import jsonify, request
from app.models.schedule import Schedule

class ScheduleController:
    """Controller xử lý logic cho Lịch học"""
    
    @staticmethod
    def get_schedule_by_student(ma_sv):
        """Lấy thời khóa biểu của sinh viên"""
        try:
            schedules = Schedule.get_by_student(ma_sv)
            return jsonify({
                'success': True,
                'data': schedules,
                'total': len(schedules)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_schedule_by_day(ma_sv, thu):
        """Lấy lịch học theo ngày"""
        try:
            schedules = Schedule.get_by_day(ma_sv, thu)
            return jsonify({
                'success': True,
                'data': schedules,
                'total': len(schedules)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_schedule(ma_lh):
        """Lấy thông tin một lịch học"""
        try:
            schedule = Schedule.get_by_id(ma_lh)
            if not schedule:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch học'
                }), 404
            
            return jsonify({
                'success': True,
                'data': schedule
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_schedule():
        """Tạo lịch học mới"""
        try:
            data = request.get_json()
            
            # Validate
            required_fields = ['ma_sv', 'ma_mh', 'thu', 'gio_bat_dau', 'gio_ket_thuc']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'Thiếu thông tin bắt buộc: {field}'
                    }), 400
            
            # Validate thu (2-8)
            if not (2 <= int(data['thu']) <= 8):
                return jsonify({
                    'success': False,
                    'message': 'Ngày trong tuần phải từ 2 (Thứ 2) đến 8 (Chủ nhật)'
                }), 400
            
            # Tạo lịch học
            ma_lh = Schedule.create(
                ma_sv=data['ma_sv'],
                ma_mh=data['ma_mh'],
                thu=data['thu'],
                gio_bat_dau=data['gio_bat_dau'],
                gio_ket_thuc=data['gio_ket_thuc'],
                phong=data.get('phong')
            )
            
            return jsonify({
                'success': True,
                'message': 'Tạo lịch học thành công',
                'data': {'ma_lh': ma_lh}
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def update_schedule(ma_lh):
        """Cập nhật lịch học"""
        try:
            data = request.get_json()
            
            # Kiểm tra lịch học tồn tại
            schedule = Schedule.get_by_id(ma_lh)
            if not schedule:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch học'
                }), 404
            
            # Update
            success = Schedule.update(
                ma_lh=ma_lh,
                thu=data.get('thu'),
                gio_bat_dau=data.get('gio_bat_dau'),
                gio_ket_thuc=data.get('gio_ket_thuc'),
                phong=data.get('phong')
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cập nhật lịch học thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không có thay đổi nào'
                }), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def delete_schedule(ma_lh):
        """Xóa lịch học"""
        try:
            success = Schedule.delete(ma_lh)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa lịch học thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch học'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
