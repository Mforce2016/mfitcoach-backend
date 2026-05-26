from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    API_SECRET = os.getenv("API_SECRET")

    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )

    REQUEST_TIMEOUT = 60


settings = Settings()