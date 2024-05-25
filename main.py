from flask import Flask, request, send_file, jsonify
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher, Updater

app = Flask(__name__)

TOKEN = '7188910603:AAGG-9sIlhdrZ4y4ZTcoURrl5c4jqdI3zL4'
bot = Bot(token=TOKEN)

# Dictionary to store user data
users_data = {}

# Dictionary to store collected coins
collected_coins = {}

# Serve the game HTML
@app.route('/')
def index():
    return send_file('index.html')

# Webhook route to handle Telegram updates
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# Command to start the game
def start(update, context):
    chat_id = update.message.chat_id
    game_url = 'https://YOUR_REPLIT_URL'  # Replace with your Replit project URL
    bot.send_message(chat_id=chat_id, text=f"Click the link to start the game: {game_url}")

# Function to collect a coin
@app.route('/collect_coin', methods=['POST'])
def collect_coin():
    user_id = request.json.get('user_id')
    coin_id = request.json.get('coin_id')

    if coin_id in collected_coins:
        return jsonify({'status': 'fail', 'message': 'Coin already collected'})

    collected_coins[coin_id] = user_id
    if user_id not in users_data:
        users_data[user_id] = {'points': 0}
    users_data[user_id]['points'] += 10  # Reward for collecting a coin

    return jsonify({'status': 'success', 'message': f'Coin {coin_id} collected'})

# Set up the updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
