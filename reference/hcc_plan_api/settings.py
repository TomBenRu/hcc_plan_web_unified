from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Reads the variables of the most recent .env file in hirarchy. Variable names are not case sensitiv."""
    provider: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_actors: str
    supervisor_username: str
    supervisor_password: str

    # postgresql on render.com
    provider_sql: str
    host_sql: str
    user_sql: str
    database_sql: str
    password_sql: str

    # to send emails
    send_address: str
    send_password: str
    post_ausg_server: str
    send_port: int

    class Config:
        env_file = '.env'


try:
    settings = Settings()
except Exception as e:
    print(f'Trying to get Settings from Environment:\n{e}\nNow I check the .env-file:')
    settings = Settings(_env_file='.env')
