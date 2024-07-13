from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import InvalidSignatureError
import psycopg2
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
# SUPABASE_KEY = os.getenv('SUPABASE_KEY')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Initialize MessagingApi and WebhookHandler
config = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(config)
messaging_api = MessagingApi(api_client)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(SUPABASE_URL)
    return conn

@app.route("/", methods=['GET'])
def home():
    return "Hello, this is the Line bot server!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        app.logger.error(f"Invalid signature error: {e}")
        abort(400)
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # user_id = event.source.user_id
    text = event.message.text

    # Assuming the message format is "create item_name item_description price"
    if text.lower().startswith("create"):
        try:
            _, item_name, item_description, price = text.split(maxsplit=3)
            price = float(price)
            save_item_to_db(item_name, item_description, price)
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"Item '{item_name}' created successfully!")]
                )
            )
        except ValueError as e:
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"Error: {e}. Use the format 'create item_name item_description price'")]
                )
            )

def save_item_to_db(item_name, item_description, price):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO item (name, description, price) VALUES (%s, %s, %s)",
                (item_name, item_description, price)
            )
        conn.commit()

if __name__ == "__main__":
    app.run()
