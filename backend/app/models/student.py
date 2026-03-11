from app.utils.database import Database
import uuid
from datetime import datetime

class Student:
    """Model cho bảng SINHVIEN"""
    
    @staticmethod
    def create(ho_ten, email, mat_khau):
        """Tạo sinh viên mới"""
        ma_sv = f"SV{str(uuid.uuid4())[:8].upper()}"
        
        query = """
            INSERT INTO SINHVIEN (MASV, HO_TEN, EMAIL, MAT_KHAU, NGAY_TAO, NGAY_CAP_NHAT)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (ma_sv, ho_ten, email, mat_khau, datetime.now(), datetime.now())
        
        Database.execute_query(query, params, fetch=False)
        return ma_sv
    
    @staticmethod
    def get_by_id(ma_sv):
        """Lấy thông tin sinh viên theo mã"""
        query = "SELECT * FROM SINHVIEN WHERE MASV = ?"
        results = Database.execute_query(query, (ma_sv,))
        return results[0] if results else None
    
    @staticmethod
    def get_by_email(email):
        """Lấy thông tin sinh viên theo email"""
        query = "SELECT * FROM SINHVIEN WHERE EMAIL = ?"
        results = Database.execute_query(query, (email,))
        return results[0] if results else None
    
    @staticmethod
    def get_all():
        """Lấy tất cả sinh viên"""
        query = "SELECT MASV, HO_TEN, EMAIL, NGAY_TAO, NGAY_CAP_NHAT FROM SINHVIEN"
        return Database.execute_query(query)
    
    @staticmethod
    def update(ma_sv, ho_ten=None, email=None):
        """Cập nhật thông tin sinh viên"""
        updates = []
        params = []
        
        if ho_ten:
            updates.append("HO_TEN = ?")
            params.append(ho_ten)
        if email:
            updates.append("EMAIL = ?")
            params.append(email)
        
        if not updates:
            return False
        
        updates.append("NGAY_CAP_NHAT = ?")
        params.append(datetime.now())
        params.append(ma_sv)
        
        query = f"UPDATE SINHVIEN SET {', '.join(updates)} WHERE MASV = ?"
        rows_affected = Database.execute_query(query, params, fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def delete(ma_sv):
        """Xóa sinh viên"""
        query = "DELETE FROM SINHVIEN WHERE MASV = ?"
        rows_affected = Database.execute_query(query, (ma_sv,), fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def authenticate(email, mat_khau):
        """Xác thực đăng nhập"""
        query = "SELECT * FROM SINHVIEN WHERE EMAIL = ? AND MAT_KHAU = ?"
        results = Database.execute_query(query, (email, mat_khau))
        return results[0] if results else None