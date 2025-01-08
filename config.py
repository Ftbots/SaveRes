import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8153366664:AAFja6tp8BZZL51GzQmZmCfEc_H3mxo1Rbo")
API_ID = int(os.environ.get("API_ID", "24994752"))
API_HASH = os.environ.get("API_HASH", "1c9b10f27f4ab2811ed4f102cc005837")
DB_URI = os.environ.get("DB_URI", "mongodb+srv://suryabhai991100:pPmTrc0DoyPsEcmn@cluster0.xpua4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
ADMINS = list(map(int, os.environ.get("ADMINS", "6104201545 7870803769 6104201545").split()))
DUMP = int(os.environ.get("DUMP", "-1002368509718"))
