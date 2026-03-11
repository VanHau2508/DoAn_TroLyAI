from flask import jsonify, request
from app.models.deadline import Deadline

class DeadlineController:
    """Controller xử lý logic cho Deadline"""
    
    @staticmethod
    def get_deadlines_by_student(ma_sv):
        """Lấy tất cả deadline của sinh viên"""
        try:
            # Lấy tham số trang_thai từ query string (optional)
            trang_thai = request.args.get('trang_thai', type=int)
            
            deadlines = Deadline.get_by_student(ma_sv, trang_thai)
            return jsonify({
                'success': True,
                'data': deadlines,
                'total': len(deadlines)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_upcoming_deadlines(ma_sv):
        """Lấy deadline sắp tới (chưa hoàn thành)"""
        try:
            deadlines = Deadline.get_upcoming(ma_sv)
            return jsonify({
                'success': True,
                'data': deadlines,
                'total': len(deadlines)
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def get_deadline(ma_dl):
        """Lấy thông tin một deadline"""
        try:
            deadline = Deadline.get_by_id(ma_dl)
            if not deadline:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy deadline'
                }), 404
            
            return jsonify({
                'success': True,
                'data': deadline
            }), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def create_deadline():
        """Tạo deadline mới"""
        try:
            data = request.get_json()
            
            # Validate
            required_fields = ['ma_sv', 'ma_mh', 'tieu_de', 'ngay_nop']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({
                        'success': False,
                        'message': f'Thiếu thông tin bắt buộc: {field}'
                    }), 400
            
            # Tạo deadline
            ma_dl = Deadline.create(
                ma_sv=data['ma_sv'],
                ma_mh=data['ma_mh'],
                tieu_de=data['tieu_de'],
                mo_ta=data.get('mo_ta'),
                ngay_nop=data['ngay_nop']
            )
            
            return jsonify({
                'success': True,
                'message': 'Tạo deadline thành công',
                'data': {'ma_dl': ma_dl}
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def mark_completed(ma_dl):
        """Đánh dấu deadline đã hoàn thành"""
        try:
            success = Deadline.mark_completed(ma_dl)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Đánh dấu hoàn thành thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy deadline'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def update_deadline(ma_dl):
        """Cập nhật deadline"""
        try:
            data = request.get_json()
            
            # Kiểm tra deadline tồn tại
            deadline = Deadline.get_by_id(ma_dl)
            if not deadline:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy deadline'
                }), 404
            
            # Update
            success = Deadline.update(
                ma_dl=ma_dl,
                tieu_de=data.get('tieu_de'),
                mo_ta=data.get('mo_ta'),
                ngay_nop=data.get('ngay_nop'),
                trang_thai=data.get('trang_thai')
            )
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Cập nhật deadline thành công'
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
    def delete_deadline(ma_dl):
        """Xóa deadline"""
        try:
            success = Deadline.delete(ma_dl)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa deadline thành công'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy deadline'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500