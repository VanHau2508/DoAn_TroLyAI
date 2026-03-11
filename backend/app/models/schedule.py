from app.utils.database import Database
import uuid
from datetime import datetime

class Schedule:
    """Model cho bảng LICH_HOC"""
    
    @staticmethod
    def create(ma_sv, ma_mh, thu, gio_bat_dau, gio_ket_thuc, phong=None):
        """Tạo lịch học mới"""
        ma_lh = f"LH{str(uuid.uuid4())[:8].upper()}"
        
        query = """
            INSERT INTO LICH_HOC (MALH, MASV, MAMH, THU, GIO_BAT_DAU, GIO_KET_THUC, PHONG, NGAY_TAO)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (ma_lh, ma_sv, ma_mh, thu, gio_bat_dau, gio_ket_thuc, phong, datetime.now())
        
        Database.execute_query(query, params, fetch=False)
        return ma_lh
    
    @staticmethod
    def get_by_student(ma_sv):
        """Lấy thời khóa biểu của sinh viên"""
        query = """
            SELECT lh.*, mh.TENMH 
            FROM LICH_HOC lh
            LEFT JOIN MON_HOC mh ON lh.MAMH = mh.MAMH
            WHERE lh.MASV = ?
            ORDER BY lh.THU, lh.GIO_BAT_DAU
        """
        return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_by_day(ma_sv, thu):
        """Lấy lịch học theo ngày (2=Thứ 2, 3=Thứ 3, ...)"""
        query = """
            SELECT lh.*, mh.TENMH 
            FROM LICH_HOC lh
            LEFT JOIN MON_HOC mh ON lh.MAMH = mh.MAMH
            WHERE lh.MASV = ? AND lh.THU = ?
            ORDER BY lh.GIO_BAT_DAU
        """
        return Database.execute_query(query, (ma_sv, thu))
    
    @staticmethod
    def get_by_id(ma_lh):
        """Lấy thông tin lịch học theo mã"""
        query = "SELECT * FROM LICH_HOC WHERE MALH = ?"
        results = Database.execute_query(query, (ma_lh,))
        return results[0] if results else None
    
    @staticmethod
    def update(ma_lh, thu=None, gio_bat_dau=None, gio_ket_thuc=None, phong=None):
        """Cập nhật lịch học"""
        updates = []
        params = []
        
        if thu:
            updates.append("THU = ?")
            params.append(thu)
        if gio_bat_dau:
            updates.append("GIO_BAT_DAU = ?")
            params.append(gio_bat_dau)
        if gio_ket_thuc:
            updates.append("GIO_KET_THUC = ?")
            params.append(gio_ket_thuc)
        if phong is not None:
            updates.append("PHONG = ?")
            params.append(phong)
        
        if not updates:
            return False
        
        params.append(ma_lh)
        query = f"UPDATE LICH_HOC SET {', '.join(updates)} WHERE MALH = ?"
        rows_affected = Database.execute_query(query, params, fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def delete(ma_lh):
        """Xóa lịch học"""
        query = "DELETE FROM LICH_HOC WHERE MALH = ?"
        rows_affected = Database.execute_query(query, (ma_lh,), fetch=False)
        return rows_affected > 0
