from app.utils.database import Database
import uuid
from datetime import datetime
import json

class ChatHistory:
    "Model cho bảng CHAT_HISTORY"

    @staticmethod
    def create(ma_sv, message_type, message_text, metadata=None):
        "Tạo messenger mới"
        chat_id = f"CHAT{str(uuid.uuid4())[:8].upper()}"

        query = """
            INSERT INTO CHAT_HISTORY (MA_CHAT, MASV, MESSAGE_TYPE, MESSAGE_TEXT, METADATA, CREATED_AT)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        metadata_json = json.dumps(metadata) if metadata else None
        params = (chat_id, ma_sv, message_type, message_text, metadata_json, datetime.now())

        Database.execute_query(query, params, fetch=False)
        return chat_id
    
    @staticmethod
    def get_history(ma_sv, limit=50):
        "Lấy lịch sử chat của sinh viên"
        query= """
            SELECT TOP (?) CHAT_ID, MESSAGE_TYPE, MESSAGE_TEXT, METADATA, CREATED_AT
            FROM CHAT_HISTORY
            WHERE MASV = ?
            ORDER BY CREATED_AT DESC
            """
        return Database.execute_query(query, (limit, ma_sv))
    
    @staticmethod
    def get_session_history(session_id, limit=50):
        "Lấy lịch sử chat của session (nếu có)"
        #implement nếu cần phải chia session 
        pass
    
    @staticmethod
    def delete_history(ma_sv):
        "Xóa lịch sử chat"
        query = "DELETE FROM CHAT_HISTORY WHERE MASV = ?"
        return Database.execute_query(query, (ma_sv,), fetch=False)
    
class ChatSession:
        "Model cho bảng CHAT_SESSION"

        @staticmethod
        def create(ma_sv):
            "Tạo session chat mới"
            session_id = f"SESSION{str(uuid.uuid4())[:8].upper()}"

            query = """
                INSERT INTO CHAT_SESSION (SESSION_ID, MASV, STARTED_AT, LAST_MESSAGE_AT, IS_ACTIVE)
                VALUES (?, ?, ?, ?, 1)
            """

            params = (session_id, ma_sv, datetime.now(), datetime.now())

            Database.execute_query(query, params, fetch=False)
            return session_id
        
        @staticmethod
        def get_active_session(ma_sv):
            "Lấy session đang active"
            query = """
                SELECT TOP 1 * FROM CHAT_SESSION
                WHERE MASV = ? AND IS_ACTIVE = 1
                ORDER BY LAST_MESSAGE_AT DESC
                """
            results = Database.execute_query(query, (ma_sv,))
            return results[0] if results else None

        @staticmethod
        def update_last_message(session_id):
            "Cập nhật thời gian tin nhắn cuối cùng"
            query = "UPDATE CHAT_SESSION SET IS_ACTIVE = 0 WHERE SESSION_ID = ?"
            Database.execute_query(query,(session_id,), fetch=False)

