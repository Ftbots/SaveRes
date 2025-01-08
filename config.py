import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7880541615:AAFr0DBsUOMmOn5O6839FwzRY3RXfgShbB8")
API_ID = int(os.environ.get("API_ID", "22287041"))
API_HASH = os.environ.get("API_HASH", "c149386dcd58a40fa9fe60e632e161d4")
DB_URI = os.environ.get("DB_URI", "mongodb+srv://nr385708:bs6GdimYoAzmHbRF@cluster0.xtpwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
ADMINS = list(map(int, os.environ.get("ADMINS", "7597122443 7870803769 6104201545").split()))
DUMP = int(os.environ.get("DUMP", "-1002478549413"))
