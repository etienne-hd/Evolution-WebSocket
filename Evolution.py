import logging
import requests
import re

# Logger configuration
logger = logging.getLogger(__name__)  # Create a logger object with the current module's name

formatter = logging.Formatter(
    '%(asctime)s %(message)s',  # Format log messages to include timestamp and message
    datefmt='[%H:%M:%S]'  # Set timestamp format to hours, minutes, and seconds
)

stream_handler = logging.StreamHandler()  # Handler to output logs to the console
stream_handler.setFormatter(formatter)  # Apply the formatter to the handler
logger.addHandler(stream_handler)  # Add the handler to the logger

# Color codes for terminal output
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def green(to_green: str) -> str:
    """
    Add green color formatting to a string for terminal output.

    :param to_green: The string to format.
    :return: The formatted string with green color.
    """
    return OKGREEN + to_green + ENDC

def red(to_red: str) -> str:
    """
    Add red color formatting to a string for terminal output.

    :param to_red: The string to format.
    :return: The formatted string with red color.
    """
    return FAIL + to_red + ENDC

def cyan(to_cyan: str) -> str:
    """
    Add cyan color formatting to a string for terminal output.

    :param to_cyan: The string to format.
    :return: The formatted string with cyan color.
    """
    return OKCYAN + to_cyan + ENDC

class Evolution:
    def __init__(
        self, 
        logging_level: int = logging.DEBUG
    ) -> None:
        """
        Initialize the Evolution class with logging and HTTP session setup.

        :param logging_level: Logging level for the logger.
        """
        logger.setLevel(logging_level)  # Set the logging level
        self.session = requests.Session()  # Create a new HTTP session
        # Set default headers for the HTTP session
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
            'Accept': '*/*',
            'Accept-Language': 'fr,en;q=0.8,fr-FR;q=0.6,es;q=0.4,en-US;q=0.2',
            'Origin': 'https://babylonrbt.evo-games.com',
        }

    def __hide_value__(self, value: str, level: int = 3) -> str:
        """
        Mask a part of the value for security reasons.

        :param value: The string value to mask.
        :param level: The level of masking; higher values mask more of the string.
        :return: The masked string.
        """
        if not value:
            return ''
        hide_length = int(len(value) / level)  # Determine the length of the masking
        return value[:-hide_length] + '*' * hide_length  # Return masked string

    def __extract_client_version__(self, data: str) -> str:
        """
        Extract the client version from the provided data.

        :param data: The data containing the client version.
        :return: The extracted client version or None if not found.
        """
        client_version_pattern = re.compile(r'client_version="([\d.]+-[a-z0-9]+)"')  # Regex to find client version
        match = client_version_pattern.search(data)
        if match:
            version = match.group(1)  # Extract the version from the match
            logger.debug(green(f"Client version retrieved successfully: {self.__hide_value__(version)}"))
            return version
        else:
            logger.warning(red("Client version not found in response data."))
            return None

    def __get_EVOSESSIONID__(self, response: requests.Response) -> str:
        """
        Obtain the EVOSESSIONID cookie from the response.

        :param response: The HTTP response object.
        :return: The EVOSESSIONID cookie value or None if not found.
        """
        for cookie_name, cookie_value in response.cookies.items():
            if cookie_name.strip() == "EVOSESSIONID" and cookie_value:
                logger.debug(green(f"EVOSESSIONID retrieved successfully: {self.__hide_value__(cookie_value)}"))
                return cookie_value
        return None

    def __get_config__(self, table_id: str) -> dict:
        """
        Obtain the game configuration for a given table_id.

        :param table_id: The ID of the game table.
        :return: The configuration dictionary for the game.
        :raises RuntimeError: If the configuration retrieval fails.
        """
        config_params = {
            "table_id": table_id,
            "origin": "https://babylonrbt.evo-games.com",
        }

        response = self.session.get(
            url="https://babylonrbt.evo-games.com/config",
            params=config_params
        )

        if response.status_code == 200:
            table_name = response.json().get('tableName', 'Unknown')  # Extract table name from response
            logger.debug(green(f"Game '{table_name}' found!"))
            return response.json()
        else:
            error_message = f"Failed to retrieve config: {response.status_code} - {response.text}"
            logger.error(red(error_message))
            raise RuntimeError(error_message)  # Raise an exception if the retrieval fails

    def get_websocket(
        self, 
        entry_url: str,
        table_id: str,
    ) -> str:
        """
        Obtain the WebSocket URL for a specified game.

        :param entry_url: The entry URL to access.
        :param table_id: The ID of the game table.
        :return: The WebSocket URL.
        :raises RuntimeError: If unable to retrieve the WebSocket URL.
        """
        response = self.session.get(entry_url)
        if not response.ok:
            error_message = f"Failed to access entry URL: {response.status_code} - {response.text}"
            logger.error(red(error_message))
            raise RuntimeError(error_message)  # Raise an exception if accessing the entry URL fails

        EVOSESSIONID = None
        for resp in response.history:
            EVOSESSIONID = self.__get_EVOSESSIONID__(resp)  # Extract EVOSESSIONID from response history
            if EVOSESSIONID:
                break

        if EVOSESSIONID:
            config = self.__get_config__(table_id)
            ws_url = f"wss://{config['serverHost']}{config['wsUrl']}"  # Construct WebSocket URL
            logger.debug(green(f"WebSocket URL retrieved successfully: {self.__hide_value__(ws_url, 2)}"))
            return ws_url
        else:
            error_message = "Unable to retrieve EVOSESSIONID from response history."
            logger.error(red(error_message))
            raise RuntimeError(error_message)  # Raise an exception if EVOSESSIONID is not found
