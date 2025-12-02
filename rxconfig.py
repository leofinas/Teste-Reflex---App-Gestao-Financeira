import reflex as rx
import os
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

config = rx.Config(
    app_name="app",
    plugins=[rx.plugins.TailwindV3Plugin()],
    env={
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID"),
        "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET"),
        # adicione outras se precisar
    }
)
