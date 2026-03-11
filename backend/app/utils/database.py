import pyodbc
from app.config.config import Config
from datetime import datetime, date

class Database:
    """Database connection handler"""
    
    @staticmethod
    def get_connection():
        """Tạo kết nối đến SQL Server"""
        try:
            # Connection string tối ưu cho ODBC Driver 17
            connection_string = (
                f"DRIVER={{{Config.DB_DRIVER}}};"
                f"SERVER={Config.DB_SERVER};"
                f"DATABASE={Config.DB_NAME};"
                f"UID={Config.DB_USERNAME};"
                f"PWD={Config.DB_PASSWORD};"
                f"Encrypt=no;"  # Driver 17 không bắt buộc encrypt
            )
            
            print(f"🔗 Connecting to: {Config.DB_SERVER}/{Config.DB_NAME}")
            print(f"🔧 Driver: {Config.DB_DRIVER}")
            
            conn = pyodbc.connect(connection_string, timeout=10)
            print("✅ Database connection successful!")
            return conn
            
        except pyodbc.Error as e:
            print(f"❌ Database connection error:")
            print(f"   Error: {e}")
            print(f"   Server: {Config.DB_SERVER}")
            print(f"   Database: {Config.DB_NAME}")
            print(f"   Driver: {Config.DB_DRIVER}")
            raise
    
    @staticmethod
    def serialize_value(value):
        """Chuyển đổi các kiểu dữ liệu đặc biệt sang JSON-serializable"""
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value
    
    @staticmethod
    def execute_query(query, params=None, fetch=True):
        """Thực thi SQL query"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                # Fetch results
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    # Serialize datetime objects
                    row_dict = {}
                    for i, column in enumerate(columns):
                        row_dict[column] = Database.serialize_value(row[i])
                    results.append(row_dict)
                return results
            else:
                # Commit changes
                conn.commit()
                return cursor.rowcount
                
        except pyodbc.Error as e:
            if conn:
                conn.rollback()
            print(f"❌ Query execution error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()