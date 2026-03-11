from app.utils.database import Database
import uuid
from datetime import datetime

class Deadline:
    """Model cho bảng DEADLINE"""
    
    @staticmethod
    def create(ma_sv, ma_mh, tieu_de, mo_ta=None, ngay_nop=None):
        """Tạo deadline mới"""
        ma_dl = f"DL{str(uuid.uuid4())[:8].upper()}"
        
        # Parse ngay_nop nếu là string
        if isinstance(ngay_nop, str):
            try:
                # Parse từ HTML datetime-local format: "2026-03-15T23:59"
                ngay_nop = datetime.strptime(ngay_nop, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    # Thử format khác: "2026-03-15 23:59:00"
                    ngay_nop = datetime.strptime(ngay_nop, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # Thử format ISO: "2026-03-15T23:59:00"
                    ngay_nop = datetime.fromisoformat(ngay_nop.replace('Z', '+00:00'))
        
        query = """
            INSERT INTO DEADLINE (MADL, MAMH, MASV, TIEU_DE, MO_TA, NGAY_NOP, TRANG_THAI, NGAY_TAO)
            VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        """
        params = (ma_dl, ma_mh, ma_sv, tieu_de, mo_ta, ngay_nop, datetime.now())
        
        Database.execute_query(query, params, fetch=False)
        return ma_dl
    
    @staticmethod
    def get_by_student(ma_sv, trang_thai=None):
        """Lấy deadline của sinh viên"""
        if trang_thai is not None:
            query = """
                SELECT d.*, mh.TENMH 
                FROM DEADLINE d
                LEFT JOIN MON_HOC mh ON d.MAMH = mh.MAMH
                WHERE d.MASV = ? AND d.TRANG_THAI = ?
                ORDER BY d.NGAY_NOP
            """
            return Database.execute_query(query, (ma_sv, trang_thai))
        else:
            query = """
                SELECT d.*, mh.TENMH 
                FROM DEADLINE d
                LEFT JOIN MON_HOC mh ON d.MAMH = mh.MAMH
                WHERE d.MASV = ?
                ORDER BY d.NGAY_NOP
            """
            return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_upcoming(ma_sv):
        """Lấy deadline sắp tới (chưa hoàn thành)"""
        query = """
            SELECT d.*, mh.TENMH 
            FROM DEADLINE d
            LEFT JOIN MON_HOC mh ON d.MAMH = mh.MAMH
            WHERE d.MASV = ? AND d.TRANG_THAI = 0 AND d.NGAY_NOP >= GETDATE()
            ORDER BY d.NGAY_NOP
        """
        return Database.execute_query(query, (ma_sv,))
    
    @staticmethod
    def get_by_id(ma_dl):
        """Lấy thông tin deadline theo mã"""
        query = "SELECT * FROM DEADLINE WHERE MADL = ?"
        results = Database.execute_query(query, (ma_dl,))
        return results[0] if results else None
    
    @staticmethod
    def mark_completed(ma_dl):
        """Đánh dấu deadline đã hoàn thành"""
        query = "UPDATE DEADLINE SET TRANG_THAI = 1 WHERE MADL = ?"
        rows_affected = Database.execute_query(query, (ma_dl,), fetch=False)
        print(f"✅ Rows affected: {rows_affected}")
        return rows_affected > 0
    
    @staticmethod
    def update(ma_dl, tieu_de=None, mo_ta=None, ngay_nop=None, trang_thai=None):
        """Cập nhật deadline"""
        updates = []
        params = []
        
        if tieu_de:
            updates.append("TIEU_DE = ?")
            params.append(tieu_de)
        if mo_ta is not None:
            updates.append("MO_TA = ?")
            params.append(mo_ta)
        if ngay_nop is not None:
            # Parse ngay_nop nếu là string
            if isinstance(ngay_nop, str):
                try:
                    ngay_nop = datetime.strptime(ngay_nop, '%Y-%m-%dT%H:%M')
                except ValueError:
                    try:
                        ngay_nop = datetime.strptime(ngay_nop, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        ngay_nop = datetime.fromisoformat(ngay_nop.replace('Z', '+00:00'))
            
            updates.append("NGAY_NOP = ?")
            params.append(ngay_nop)
        if trang_thai is not None:
            updates.append("TRANG_THAI = ?")
            params.append(trang_thai)
        
        if not updates:
            return False
        
        params.append(ma_dl)
        query = f"UPDATE DEADLINE SET {', '.join(updates)} WHERE MADL = ?"
        rows_affected = Database.execute_query(query, params, fetch=False)
        return rows_affected > 0
    
    @staticmethod
    def delete(ma_dl):
        """Xóa deadline"""
        query = "DELETE FROM DEADLINE WHERE MADL = ?"
        rows_affected = Database.execute_query(query, (ma_dl,), fetch=False)
        return rows_affected > 0