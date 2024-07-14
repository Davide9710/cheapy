from linebot.v3.messaging import TextMessage

def create_text_response(text):
    return TextMessage(text=text)