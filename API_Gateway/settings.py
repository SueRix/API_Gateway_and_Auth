import os


class Settings:
    AUTH_SERVICE_URL: str = os.getenv('AUTH_SERVICE_URL', 'http://djangoapp:8002')
    CALENDAR_SERVICE_URL: str = os.getenv('CALENDAR_SERVICE_URL', 'http://5000')
    #TODO: Overwrite this class BASESETTINGS Pydentic to avoid os getenv.
    #TODO: Create env file to store these variables
    class Config:
        env_file = ".env"


settings = Settings()
