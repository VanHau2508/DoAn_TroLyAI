from flask import Flask
from flask_cors import CORS
from app.config.config import config

def create_app(config_name='development'):
    """Factory function để tạo Flask app"""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # ✅ FIX: Disable strict slashes globally (CẤU HÌNH TOÀN CỤC)
    app.url_map.strict_slashes = False
    
    # Enable CORS with specific config
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5500", "null"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    print("🔧 Đang đăng ký blueprints...")
    
    # Register blueprints
    try:
        from app.routes.student_routes import student_bp
        app.register_blueprint(student_bp)
        print("✅ Đã đăng ký student_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký student_bp: {e}")
    
    try:
        from app.routes.subject_routes import subject_bp
        app.register_blueprint(subject_bp)
        print("✅ Đã đăng ký subject_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký subject_bp: {e}")
    
    try:
        from app.routes.schedule_routes import schedule_bp
        app.register_blueprint(schedule_bp)
        print("✅ Đã đăng ký schedule_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký schedule_bp: {e}")
    
    try:
        from app.routes.exam_routes import exam_bp
        app.register_blueprint(exam_bp)
        print("✅ Đã đăng ký exam_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký exam_bp: {e}")
    
    try:
        from app.routes.deadline_routes import deadline_bp
        app.register_blueprint(deadline_bp)
        print("✅ Đã đăng ký deadline_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký deadline_bp: {e}")
    
    print("🎉 Hoàn tất đăng ký blueprints!")

    try:
        from app.routes.chat_routes import chat_bp
        app.register_blueprint(chat_bp)
        print("✅ Đã đăng ký chat_bp")
    except Exception as e:
        print(f"❌ Lỗi đăng ký chat_bp: {e}")
    
    # Health check route
    @app.route('/')
    def index():
        return {
            'success': True,
            'message': '🎓 Student Assistant API is running!',
            'version': '1.0.0',
            'endpoints': {
                'students': '/api/students',
                'subjects': '/api/subjects',
                'schedules': '/api/schedules',
                'exams': '/api/exams',
                'deadlines': '/api/deadlines',
                'api_docs': '/api'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Test database connection
    @app.route('/test-db')
    def test_db():
        try:
            from app.utils.database import Database
            conn = Database.get_connection()
            conn.close()
            return {
                'success': True,
                'message': '✅ Kết nối database thành công!'
            }, 200
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Lỗi kết nối database: {str(e)}'
            }, 500
    
    # API documentation route
    @app.route('/api')
    def api_docs():
        return {
            'success': True,
            'api_version': '1.0.0',
            'base_url': 'http://localhost:5000',
            'endpoints': {
                'Students (Sinh viên)': {
                    'GET /api/students': 'Lấy tất cả sinh viên',
                    'GET /api/students/<ma_sv>': 'Lấy một sinh viên',
                    'POST /api/students': 'Tạo sinh viên mới',
                    'POST /api/students/login': 'Đăng nhập',
                    'PUT /api/students/<ma_sv>': 'Cập nhật sinh viên',
                    'DELETE /api/students/<ma_sv>': 'Xóa sinh viên'
                },
                'Subjects (Môn học)': {
                    'GET /api/subjects': 'Lấy tất cả môn học',
                    'GET /api/subjects/student/<ma_sv>': 'Lấy môn học của sinh viên',
                    'GET /api/subjects/<ma_mh>': 'Lấy một môn học',
                    'POST /api/subjects': 'Tạo môn học mới',
                    'PUT /api/subjects/<ma_mh>': 'Cập nhật môn học',
                    'DELETE /api/subjects/<ma_mh>': 'Xóa môn học'
                },
                'Schedules (Lịch học)': {
                    'GET /api/schedules/student/<ma_sv>': 'Lấy thời khóa biểu',
                    'GET /api/schedules/student/<ma_sv>/day/<thu>': 'Lấy lịch theo ngày (2=T2, 8=CN)',
                    'GET /api/schedules/<ma_lh>': 'Lấy một lịch học',
                    'POST /api/schedules': 'Tạo lịch học mới',
                    'PUT /api/schedules/<ma_lh>': 'Cập nhật lịch học',
                    'DELETE /api/schedules/<ma_lh>': 'Xóa lịch học'
                },
                'Exams (Lịch thi)': {
                    'GET /api/exams/student/<ma_sv>': 'Lấy tất cả lịch thi',
                    'GET /api/exams/student/<ma_sv>/upcoming': 'Lấy lịch thi sắp tới',
                    'GET /api/exams/<ma_lt>': 'Lấy một lịch thi',
                    'POST /api/exams': 'Tạo lịch thi mới',
                    'PUT /api/exams/<ma_lt>': 'Cập nhật lịch thi',
                    'DELETE /api/exams/<ma_lt>': 'Xóa lịch thi'
                },
                'Deadlines (Hạn nộp)': {
                    'GET /api/deadlines/student/<ma_sv>': 'Lấy tất cả deadline',
                    'GET /api/deadlines/student/<ma_sv>/upcoming': 'Lấy deadline sắp tới',
                    'GET /api/deadlines/<ma_dl>': 'Lấy một deadline',
                    'POST /api/deadlines': 'Tạo deadline mới',
                    'PUT /api/deadlines/<ma_dl>/complete': 'Đánh dấu hoàn thành',
                    'PUT /api/deadlines/<ma_dl>': 'Cập nhật deadline',
                    'DELETE /api/deadlines/<ma_dl>': 'Xóa deadline'
                }
            }
        }
    
    return app