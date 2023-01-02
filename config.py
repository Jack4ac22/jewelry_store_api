from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    expiration_minutes: int
    email_address: str
    email_password: str
    host_name: str

    class Config:
        env_file = ".env"


settings = Settings()
