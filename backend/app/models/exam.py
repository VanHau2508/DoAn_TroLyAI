from app.utils.database import Database
import uuid
from datetime import datetime

class Exam:
    """Model cho bảng LICH_THI"""
    
    @staticmethod
    def create(ma_sv, ma_mh, ngay_thi, phong_thi=None, hinh_thuc=None):
        """Tạo lịch thi mới"""
        ma_lt = f"LT{str(uuid.uuid4())[:8].upper()}"
        
        query = """
            INSERT INTO LICH_THI (MALT, MAMH, MASV, NGAY_THI, PHONG_THI, HINH_THUC, NGAY_TAO)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (ma_lt, ma_mh, ma_sv, ngay_thi, phong_thi, hinh_thuc, datetime.now())
        
        Database.execute_query(query, params, fetch=False)
        return ma_lt
    
    @staticmethod
    def get_by_student(ma_sv):
        """Lấy lịch thi của sinh viên"""
        query = """
            SELECT lt.*, mh.TENMH 
            FROM LICH_THI lt
            LEFT JOIN MON_HOC mh ON lt.MAMH = mh.MAMH
            WHERE lt.MASV = ?
            ORDER BY lt.NGAY_THI
        """
        return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_upcoming(ma_sv):
        """Lấy lịch thi sắp tới"""
        query = """
            SELECT lt.*, mh.TENMH 
            FROM LICH_THI lt
            LEFT JOIN MON_HOC mh ON lt.MAMH = mh.MAMH
            WHERE lt.MASV = ? AND lt.NGAY_THI >= GETDATE()
            ORDER BY lt.NGAY_THI
        """
        return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_by_id(ma_lt):
        """Lấy thông tin lịch thi theo mã"""
        query = "SELECT * FROM LICH_THI WHERE MALT = ?"
        results = Database.execute_query(query, (ma_lt,))
        return results[0] if results else None
    
    @staticmethod
    def update(ma_lt, ngay_thi=None, phong_thi=None, hinh_thuc=None):
        """Cập nhật lịch thi"""
        updates = []
        params = []
        
        if ngay_thi:
            updates.append("NGAY_THI = ?")
            params.append(ngay_thi)
        if phong_thi is not None:
            updates.append("PHONG_THI = ?")
            params.append(phong_thi)
        if hinh_thuc is not None:
            updates.append("HINH_THUC = ?")
            params.append(hinh_thuc)
        
        if not updates:
            return False
        
        params.append(ma_lt)
        query = f"UPDATE LICH_THI SET {', '.join(updates)} WHERE MALT = ?"
        rows_affected = Database.execute_query(query, params, fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def delete(ma_lt):
        """Xóa lịch thi"""
        query = "DELETE FROM LICH_THI WHERE MALT = ?"
        rows_affected = Database.execute_query(query, (ma_lt,), fetch=False)
        return rows_affected > 0
