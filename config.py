import os

api = os.getenv('Chat_GPT_API')
bot_token = os.getenv('BOT_TOKEN')
mongodb_uri = f"mongodb://mongo:{os.getenv('MONGODB_PORT')}"


