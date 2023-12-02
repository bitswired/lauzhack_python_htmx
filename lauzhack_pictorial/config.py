from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from a .env file into the environment
load_dotenv()


class Config(BaseSettings):
    """
    Configuration class to handle enviroment variables.

    Inherits from BaseSettings, which is a Pydantic model designed to read
    and validate environment variables. The Config class defines expected
    environment variables and their corresponding types. When an instance
    of Config is created, Pydantic will automatically read the corresponding
    environment variables, cast them to the defined type, and validate them.

    Attributes:
        DATABASE_URL (str): Database connection URL read from the DATABASE_URL
                            environment variable. Required to configure the
                            database connection for the application.

    Example usage within application:
        - To access the DATABASE_URL, assuming an instance of Config named CONFIG:
            ```
            database_connection_url = CONFIG.DATABASE_URL
            ```
        - To initialize CONFIG at the start of your main application script:
            ```
            CONFIG = Config()
            ```
    """

    DATABASE_URL: str


# Create a Config instance to load and hold our environment-based configuration
CONFIG = Config()
