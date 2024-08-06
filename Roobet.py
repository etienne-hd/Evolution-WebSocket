import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize logger for the module
logger = logging.getLogger(__name__)

# Define the format for logging messages
formatter = logging.Formatter(
    '%(asctime)s %(message)s',
    datefmt='[%H:%M:%S]'
)

# Create a stream handler for logging to the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Define color codes for terminal output
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def green(to_green: str) -> str:
    """
    Apply green color to a string for terminal output.

    :param to_green: String to be colored green.
    :return: The input string wrapped with green color codes.
    """
    return OKGREEN + to_green + ENDC

def red(to_red: str) -> str:
    """
    Apply red color to a string for terminal output.

    :param to_red: String to be colored red.
    :return: The input string wrapped with red color codes.
    """
    return FAIL + to_red + ENDC

class Roobet:
    def __init__(
        self, 
        sid=None,
        logging_level: logging = logging.DEBUG
    ) -> None:
        """
        Initialize the Roobet class instance.

        :param sid: Session ID for authentication. If not provided, it will be retrieved from environment variables.
        :param logging_level: The logging level to set for the logger (default is DEBUG).
        :raises ValueError: If SID is not provided and cannot be retrieved from environment variables.
        """
        logger.setLevel(logging_level)
        self.session = requests.Session()

        # Retrieve session ID from environment variables if not provided
        sid = sid or os.getenv('SID')
        if sid:
            self.session.cookies.set('connect.sid', sid)
        else:
            error_message = "SID not provided. Please set the SID environment variable or pass it as an argument."
            logger.error(red(error_message))
            raise ValueError(error_message)
        
        # Set default headers for HTTP requests
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'fr',
            'Connection': 'keep-alive',
            'Priority': 'u=4',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

    def get_entry_url(
        self, 
        name: str, 
        currency: str = "USD"
    ) -> str:
        """
        Retrieve the URL for a game from the Roobet API.

        :param name: Name of the game to retrieve.
        :param currency: Currency to be used (default is "USD").
        :return: The URL to launch the game.
        :raises ValueError: If the game URL is not found in the response.
        :raises RuntimeError: If there is an error in the HTTP request.
        """
        params = {
            "gameName": f"evolution:{name}",
            "type": "desktop",
            "currency": currency
        }

        # Send a GET request to the Roobet API
        response = self.session.get(
            url='https://roobet.com/_api/softswiss/getGameLink',
            params=params
        )

        if response.status_code == 200:
            # Extract game URL from the JSON response
            game_url = response.json().get('launch_options', {}).get('game_url', '')
            if game_url:
                logger.info(green(f"Successfully retrieved game URL: {game_url}"))
                return game_url
            else:
                error_message = "Game URL not found in response."
                logger.error(red(error_message))
                raise ValueError(error_message)
        else:
            error_message = f"Error retrieving game URL: {response.status_code} - {response.text}"
            logger.error(red(error_message))
            raise RuntimeError(error_message)
