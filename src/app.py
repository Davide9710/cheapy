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
from supabase import create_client, Client
import psycopg2
import os
from .item import Item

app = Flask(__name__)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Initialize MessagingApi and WebhookHandler
config = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(config)
messaging_api = MessagingApi(api_client)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Connect to the database
def get_db_connection():
    conn = psycopg2.connect(SUPABASE_URL)
    print(f'SUPABASE_URL: {SUPABASE_URL}')
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
            item = Item(item_name, item_description, price)
            item.save_to_db(supabase)
            messaging_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"Item '{item_name}' created successfully! dev")]
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

def save_item_to_db(item_name, item_description, price):
    response = supabase.table("item").insert({"name": item_name, "description": item_description, "price": price}).execute()
    if response.status_code != 201:
        raise Exception(f"Failed to insert item: {response.status_code}")


if __name__ == "__main__":
    app.run()
