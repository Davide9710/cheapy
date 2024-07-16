from linebot.v3.messaging import MessagingApi, ReplyMessageRequest
from commands import get_command
from states import get_state
from models import User
from views import create_text_response

users = {}  # In-memory user storage, storing the state of the conversation. Stores item partial data during convers.

def handle_message(event, line_bot_api: MessagingApi):
    user_id = event.source.user_id
    user = users.get(user_id, User(id=user_id, name="Unknown"))
    
    message = event.message.text
    
    if message.startswith('/'):
        command = get_command(message[1:])
        response = command.execute(user)
    else:
        state = get_state(user.state)
        response, new_state = state.handle(user, message)
        user.state = new_state
    
    users[user_id] = user
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[create_text_response(response)]
        )
    )