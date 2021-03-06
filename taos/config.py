"""
Configuration Module:
    Config module loads commonly used environment variables
    for Taos CLI usage

    - TAOS_WEB_USER_AGENT
    - SUPPORT_EMAIL
    - CONTACT_EMAIL
    - CONTACT_ENDPOINT
    - CONTACT_WEB_SITE
    - SEND_GRID_API_KEY
    - SLACK_API_TOKEN

"""

import os

USER_AGENT = os.getenv("TAOS_WEB_USER_AGENT", "Mozilla/5.0")

SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "amcchesney@taos.com")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL")
CONTACT_ENDPOINT = os.getenv("CONTACT_ENDPOINT")
CONTACT_WEB_SITE = os.getenv(
    "CONTACT_WEB_SITE", "https://www.taos.com/contact-taos")

SEND_GRID_API_KEY = os.getenv("SEND_GRID_API_KEY")

SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
