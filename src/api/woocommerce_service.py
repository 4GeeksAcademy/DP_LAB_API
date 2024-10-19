import os
from dotenv import load_dotenv
from woocommerce import API

# Cargar las variables de entorno
load_dotenv()

def get_woocommerce_api():
    wcapi = API(
        url=os.getenv("WOOCOMMERCE_URL"),
        consumer_key=os.getenv("WOOCOMMERCE_CONSUMER_KEY"),
        consumer_secret=os.getenv("WOOCOMMERCE_CONSUMER_SECRET"),
        version="wc/v3"
    )
    return wcapi