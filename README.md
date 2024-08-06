This project is a Python script designed to retrieve WebSocket URLs for Evolution gaming platform's casino games via Roobet. The script follows several steps to authenticate with Roobet, retrieve the game URL, extract necessary configurations, and finally obtain the WebSocket URL for a specified game.

### How It Works

1. **Initialization**:
   - **Roobet Class**: Initializes with a session ID (SID) obtained either from environment variables or passed directly. Sets up HTTP headers and logging.
   - **Evolution Class**: Sets up HTTP headers and logging for subsequent requests to the Evolution game server.

2. **Authentication**:
   - The `Roobet` class uses the provided SID to authenticate with Roobet by setting it in the session cookies.

3. **Retrieve Game URL**:
   - The `get_entry_url` method in the `Roobet` class sends a GET request to Roobet's API to retrieve the game URL for a specified game name and currency.

4. **Access Entry URL**:
   - The `Evolution` class accesses the entry URL obtained from Roobet to initiate a session with Evolution.

5. **Extract EVOSESSIONID**:
   - The `__get_EVOSESSIONID__` method extracts the `EVOSESSIONID` cookie from the HTTP response history.

6. **Retrieve Game Configuration**:
   - The `__get_config__` method sends a GET request to the Evolution server to retrieve the configuration for the specified game table ID, including server host and WebSocket URL.

7. **Generate WebSocket URL**:
   - The `get_websocket` method constructs and returns the WebSocket URL using the retrieved configuration and `EVOSESSIONID`.

### Step-by-Step Code Explanation

1. **Initialization**:
   ```python
   roobet = Roobet()  # Initializes the Roobet class with SID from environment variables
   evolution = Evolution()  # Initializes the Evolution class
   ```

2. **Retrieve Game URL**:
   ```python
   game_url = roobet.get_entry_url(name="crazytime")  # Retrieves the entry URL for the CrazyTime game
   ```

3. **Access Entry URL and Extract WebSocket URL**:
   ```python
   ws_url = evolution.get_websocket(entry_url=game_url, table_id="CrazyTime0000001")  # Retrieves the WebSocket URL
   print(f"WebSocket URL: {ws_url}")  # Prints the WebSocket URL
   ```

### Example Usage for CrazyTime Game

Below is a complete example of using the script to get the WebSocket URL for the Crazy Time game with table ID `CrazyTime0000001`:

```python
import logging
from Roobet import Roobet
from Evolution import Evolution

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Roobet with SID from environment variables or directly
roobet = Roobet()

# Retrieve the entry URL for the CrazyTime game
game_url = roobet.get_entry_url(name="crazytime")

# Initialize Evolution
evolution = Evolution()

# Retrieve the WebSocket URL for CrazyTime with table ID "CrazyTime0000001"
ws_url = evolution.get_websocket(entry_url=game_url, table_id="CrazyTime0000001")

# Print the WebSocket URL
print(f"WebSocket URL: {ws_url}")
```

### Summary

- **Roobet Class**:
  - Authenticates with Roobet using SID.
  - Retrieves game entry URL from Roobet API.

- **Evolution Class**:
  - Accesses game entry URL.
  - Extracts `EVOSESSIONID`.
  - Retrieves game configuration using table ID.
  - Constructs and returns WebSocket URL.

This detailed process ensures that you can easily retrieve the WebSocket URL needed to connect to any Evolution game via Roobet.

### License

This project is licensed under the MIT License.