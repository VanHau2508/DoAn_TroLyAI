from flask import jsonify, request
from app.models.subject import Subject

class SubjectController:
    """Controller xử lý logic cho Môn học"""
    
    @staticmethod
    def get_all_subjects():
        """Lấy tất cả môn học"""
        try:
            subjects = Subject.get_all()
            return jsonify({
                'success': True,
                'data': subjects,
                'total': len(subjects)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_subjects_by_student(ma_sv):
        """Lấy môn học của sinh viên"""
        try:
            subjects = Subject.get_by_student(ma_sv)
            return jsonify({
                'success': True,
                'data': subjects,
                'total': len(subjects)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_subject(ma_mh):
        """Lấy thông tin một môn học"""
        try:
            subject = Subject.get_by_id(ma_mh)
            if not subject:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy môn học'
                }), 404
            
            return jsonify({
                'success': True,
                'data': subject
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_subject():
        """Tạo môn học mới"""
        try:
            data = request.get_json()
            
            # Validate
            if not data.get('ma_sv') or not data.get('ten_mh'):
                return jsonify({
                    'success': False,
                    'message': 'Thiếu thông tin bắt buộc (ma_sv, ten_mh)'
                }), 400
            
            # Tạo môn học
            ma_mh = Subject.create(
                ma_sv=data['ma_sv'],
                ten_mh=data['ten_mh'],
                mo_ta=data.get('mo_ta'),
                so_tin_chi=data.get('so_tin_chi', 3)
            )
            
            return jsonify({
                'success': True,
                'message': 'Tạo môn học thành công',
                'data': {'ma_mh': ma_mh}
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def update_subject(ma_mh):
        """Cập nhật môn học"""
        try:
            data = request.get_json()
            
            # Kiểm tra môn học tồn tại
            subject = Subject.get_by_id(ma_mh)
            if not subject:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy môn học'
                }), 404
            
            # Update
            success = Subject.update(
                ma_mh=ma_mh,
                ten_mh=data.get('ten_mh'),
                mo_ta=data.get('mo_ta'),
                so_tin_chi=data.get('so_tin_chi')
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cập nhật môn học thành công'
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
    def delete_subject(ma_mh):
        """Xóa môn học"""
        try:
            success = Subject.delete(ma_mh)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa môn học thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy môn học'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
