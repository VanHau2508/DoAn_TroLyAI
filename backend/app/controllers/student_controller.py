from flask import jsonify, request
from app.models.student import Student

class StudentController:
    """Controller xử lý logic cho Student"""
    
    @staticmethod
    def get_all_students():
        """Lấy danh sách tất cả sinh viên"""
        try:
            students = Student.get_all()
            return jsonify({
                'success': True,
                'data': students,
                'total': len(students)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_student(ma_sv):
        """Lấy thông tin một sinh viên"""
        try:
            student = Student.get_by_id(ma_sv)
            if not student:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy sinh viên'
                }), 404
            
            # Xóa mật khẩu trước khi trả về
            student.pop('MAT_KHAU', None)
            
            return jsonify({
                'success': True,
                'data': student
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_student():
        """Tạo sinh viên mới"""
        try:
            data = request.get_json()
            
            # Validate
            if not data.get('ho_ten') or not data.get('email') or not data.get('mat_khau'):
                return jsonify({
                    'success': False,
                    'message': 'Thiếu thông tin bắt buộc (ho_ten, email, mat_khau)'
                }), 400
            
            # Kiểm tra email đã tồn tại
            existing = Student.get_by_email(data['email'])
            if existing:
                return jsonify({
                    'success': False,
                    'message': 'Email đã được sử dụng'
                }), 400
            
            # Tạo sinh viên
            ma_sv = Student.create(
                ho_ten=data['ho_ten'],
                email=data['email'],
                mat_khau=data['mat_khau']
            )
            
            return jsonify({
                'success': True,
                'message': 'Tạo sinh viên thành công',
                'data': {'ma_sv': ma_sv}
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def update_student(ma_sv):
        """Cập nhật thông tin sinh viên"""
        try:
            data = request.get_json()
            
            # Kiểm tra sinh viên tồn tại
            student = Student.get_by_id(ma_sv)
            if not student:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy sinh viên'
                }), 404
            
            # Update
            success = Student.update(
                ma_sv=ma_sv,
                ho_ten=data.get('ho_ten'),
                email=data.get('email')
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cập nhật thành công'
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
    def delete_student(ma_sv):
        """Xóa sinh viên"""
        try:
            success = Student.delete(ma_sv)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa sinh viên thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy sinh viên'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def login():
        """Đăng nhập"""
        try:
            data = request.get_json()
            
            if not data.get('email') or not data.get('mat_khau'):
                return jsonify({
                    'success': False,
                    'message': 'Thiếu email hoặc mật khẩu'
                }), 400
            
            student = Student.authenticate(data['email'], data['mat_khau'])
            
            if student:
                # Xóa password
                student.pop('MAT_KHAU', None)
                return jsonify({
                    'success': True,
                    'message': 'Đăng nhập thành công',
                    'data': student
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Email hoặc mật khẩu không đúng'
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
