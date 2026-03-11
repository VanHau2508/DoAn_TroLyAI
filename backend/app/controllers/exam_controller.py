from flask import jsonify, request
from app.models.exam import Exam

class ExamController:
    """Controller xử lý logic cho Lịch thi"""
    
    @staticmethod
    def get_exams_by_student(ma_sv):
        """Lấy lịch thi của sinh viên"""
        try:
            exams = Exam.get_by_student(ma_sv)
            return jsonify({
                'success': True,
                'data': exams,
                'total': len(exams)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_upcoming_exams(ma_sv):
        """Lấy lịch thi sắp tới"""
        try:
            exams = Exam.get_upcoming(ma_sv)
            return jsonify({
                'success': True,
                'data': exams,
                'total': len(exams)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_exam(ma_lt):
        """Lấy thông tin một lịch thi"""
        try:
            exam = Exam.get_by_id(ma_lt)
            if not exam:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch thi'
                }), 404
            
            return jsonify({
                'success': True,
                'data': exam
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_exam():
        """Tạo lịch thi mới"""
        try:
            data = request.get_json()
            
            # Validate
            required_fields = ['ma_sv', 'ma_mh', 'ngay_thi']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'Thiếu thông tin bắt buộc: {field}'
                    }), 400
            
            # Tạo lịch thi
            ma_lt = Exam.create(
                ma_sv=data['ma_sv'],
                ma_mh=data['ma_mh'],
                ngay_thi=data['ngay_thi'],
                phong_thi=data.get('phong_thi'),
                hinh_thuc=data.get('hinh_thuc')
            )
            
            return jsonify({
                'success': True,
                'message': 'Tạo lịch thi thành công',
                'data': {'ma_lt': ma_lt}
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def update_exam(ma_lt):
        """Cập nhật lịch thi"""
        try:
            data = request.get_json()
            
            # Kiểm tra lịch thi tồn tại
            exam = Exam.get_by_id(ma_lt)
            if not exam:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch thi'
                }), 404
            
            # Update
            success = Exam.update(
                ma_lt=ma_lt,
                ngay_thi=data.get('ngay_thi'),
                phong_thi=data.get('phong_thi'),
                hinh_thuc=data.get('hinh_thuc')
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cập nhật lịch thi thành công'
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
    def delete_exam(ma_lt):
        """Xóa lịch thi"""
        try:
            success = Exam.delete(ma_lt)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa lịch thi thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy lịch thi'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
