from app.utils.database import Database
import uuid
from datetime import datetime

class Subject:
    """Model cho bảng MON_HOC"""
    
    @staticmethod
    def create(ma_sv, ten_mh, mo_ta=None, so_tin_chi=3):
        """Tạo môn học mới"""
        ma_mh = f"MH{str(uuid.uuid4())[:8].upper()}"
        
        query = """
            INSERT INTO MON_HOC (MAMH, MASV, TENMH, MOTA, SO_TIN_CHI, NGAY_TAO, NGAY_CAP_NHAT)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (ma_mh, ma_sv, ten_mh, mo_ta, so_tin_chi, datetime.now(), datetime.now())
        
        Database.execute_query(query, params, fetch=False)
        return ma_mh
    
    @staticmethod
    def get_by_student(ma_sv):
        """Lấy tất cả môn học của sinh viên"""
        query = "SELECT * FROM MON_HOC WHERE MASV = ? ORDER BY NGAY_TAO DESC"
        return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_by_id(ma_mh):
        """Lấy thông tin môn học theo mã"""
        query = "SELECT * FROM MON_HOC WHERE MAMH = ?"
        results = Database.execute_query(query, (ma_mh,))
        return results[0] if results else None
    
    @staticmethod
    def get_all():
        """Lấy tất cả môn học"""
        query = "SELECT * FROM MON_HOC ORDER BY NGAY_TAO DESC"
        return Database.execute_query(query)
    
    @staticmethod
    def update(ma_mh, ten_mh=None, mo_ta=None, so_tin_chi=None):
        """Cập nhật môn học"""
        updates = []
        params = []
        
        if ten_mh:
            updates.append("TENMH = ?")
            params.append(ten_mh)
        if mo_ta is not None:
            updates.append("MOTA = ?")
            params.append(mo_ta)
        if so_tin_chi:
            updates.append("SO_TIN_CHI = ?")
            params.append(so_tin_chi)
        
        if not updates:
            return False
        
        updates.append("NGAY_CAP_NHAT = ?")
        params.append(datetime.now())
        params.append(ma_mh)
        
        query = f"UPDATE MON_HOC SET {', '.join(updates)} WHERE MAMH = ?"
        rows_affected = Database.execute_query(query, params, fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def delete(ma_mh):
        """Xóa môn học và tất cả dữ liệu liên quan (CASCADE)"""
        try:
            # Xóa theo thứ tự: DEADLINE -> LICH_THI -> LICH_HOC -> MON_HOC
            
            # 1. Xóa DEADLINE
            query1 = "DELETE FROM DEADLINE WHERE MAMH = ?"
            Database.execute_query(query1, (ma_mh,), fetch=False)
            print(f"✅ Đã xóa DEADLINE của môn {ma_mh}")
            
            # 2. Xóa LICH_THI
            query2 = "DELETE FROM LICH_THI WHERE MAMH = ?"
            Database.execute_query(query2, (ma_mh,), fetch=False)
            print(f"✅ Đã xóa LICH_THI của môn {ma_mh}")
            
            # 3. Xóa LICH_HOC
            query3 = "DELETE FROM LICH_HOC WHERE MAMH = ?"
            Database.execute_query(query3, (ma_mh,), fetch=False)
            print(f"✅ Đã xóa LICH_HOC của môn {ma_mh}")
            
            # 4. Xóa MON_HOC
            query4 = "DELETE FROM MON_HOC WHERE MAMH = ?"
            rows_affected = Database.execute_query(query4, (ma_mh,), fetch=False)
            print(f"✅ Đã xóa MON_HOC {ma_mh}")
            
            return rows_affected > 0
            
        except Exception as e:
            print(f"❌ Error deleting subject: {e}")
            raise