import os
from app import create_app

# Lấy config từ environment variable hoặc dùng 'development'
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("=" * 50)
    print("🚀 Starting Student Assistant API...")
    print(f"📍 Server: http://localhost:{port}")
    print(f"🔧 Environment: {config_name}")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=True)