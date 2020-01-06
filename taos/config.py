import os

SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "cmorrow@taos.com")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
CONTACT_ENDPOINT  = os.getenv("CONTACT_ENDPOINT")
CONTACT_WEB_SITE = os.getenv("CONTACT_WEB_SITE","https://www.taos.com/contact-taos")

SEND_GRID_API_KEY = os.getenv("SEND_GRID_API_KEY")

USER_AGENT = os.getenv("TAOS_WEB_USER_AGENT", "Mozilla/5.0")
