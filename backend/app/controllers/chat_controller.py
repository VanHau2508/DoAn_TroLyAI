from flask import request, jsonify
from app.models.chat import ChatHistory, ChatSession
import traceback

class ChatController:
    
    @staticmethod
    def get_chat_history(ma_sv, limit=50):
        "Lấy lịch sử chat"
        try:
            history = ChatHistory.get_history(ma_sv, limit)

            #Reverse để hiển thị tin nhắn cũ đến mới
            history.reverse()

            return jsonify({
                'success': True,
                'data': history,
                'total': len(history)
            }),200
        except Exception as e:
            print(f"❌ Error getting chat history: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @staticmethod
    def send_message():
        "Gửi message và nhận AI response"
        try:
            data = request.json
            ma_sv = data.get('ma_sv')
            message = data.get('message')

            if not ma_sv or not message:
                return jsonify({
                    'success': False,
                    'message': 'Missing ma_sv or message'
                }), 400
            # Lưu user message
            user_chat_id = ChatHistory.create(ma_sv,'user', message)
            print(f"💬 User message saved: {user_chat_id}")

            # TODO: Gọi AI service để generate response
            # Tạm thời dùng placeholder
            bot_response = f"Tôi đã nhận được câu hỏi: '{message}'. AI service đang được xây dựng..."

            #LƯU BOT RESPONSE
            bot_chat_id = ChatHistory.create(ma_sv,'bot', bot_response, metadata={
                'model': 'placeholder',
                'tokens': len(bot_response)
            })
            print(f"🤖 Bot response saved:{bot_chat_id}")

            #Update session
            session = ChatSession.get_active_session(ma_sv)
            if session:
                ChatSession.update_last_message(session['SESSION_ID'])

            return jsonify({
                'success': True,
                'data':{
                    'user_message':
                    {
                        'id': user_chat_id,
                        'text': message,
                        'type': 'user'
                    }
                }
            }),
        except Exception as e:
                print(f"❌ Error sending message: {e}")
                traceback.print_exc()
                return jsonify({
                    'success': False,
                    'message': str(e)
                }), 500
    
    @staticmethod
    def delete_history(ma_sv):
        "Xóa lịch sử chat"
        try:
            ChatHistory.delete_history(ma_sv)

            return jsonify({
                'success': True,
                'message': 'Đã xóa lịch sử chat'
            }), 200
        except Exception as e:
            print(f"❌ Error deleting history: {e}")
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500

    @staticmethod
    def get_or_create_session(ma_sv):
        "Lấy hoặc tạo session"
        try:
            session = ChatSession.get_active_session(ma_sv)

            if not session:
                session_id = ChatSession.create(ma_sv)
                session = {'SESSION_ID': session_id, 'MASV': ma_sv}
            
            return jsonify({
                'success': True,
                'data': session
            }), 200

        except Exception as e:
            print(f"❌ Error getting session: {e}")
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
