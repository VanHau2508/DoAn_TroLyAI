from flask import Blueprint, request, jsonify
from app.controllers.chat_controller import ChatController

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/history/<string:ma_sv>', methods=['GET'])

def get_chat_history(ma_sv):
    "GET /api/chat/history/<ma_sv> - Lấy lịch sử chat của sinh viên"
    limit = request.args.get('limit', 50, type=int)
    return ChatController.get_chat_history(ma_sv,limit)

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """POST /api/chat/send - Gửi message và nhận response từ AI"""
    return ChatController.send_message()

@chat_bp.route('/clear/<string:ma_sv>', methods=['DELETE'])
def delete_history(ma_sv):
    """DELETE /api/chat/clear/<ma_sv> - Xóa lịch sử chat của sinh viên"""
    return ChatController.delete_history(ma_sv)

@chat_bp.route('/session/<string:ma_sv>', methods=['GET'])
def get_session(ma_sv):
    """"GET /api/chat/session/<ma_sv> - Lấy session ID hiện tại của sinh viên"""
    return ChatController.get_or_create_session(ma_sv)