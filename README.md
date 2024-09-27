# 999.md Listing Scraper  

The **999.md Listing Scraper** is a Python-based web scraper designed to extract different listing links from the 999.md website. This tool uses Selenium to automate browsing, scroll through pages, and capture relevant data while excluding irrelevant links.

---

## Features  

- **Multi-page Scraping**: Scrapes listing links across a range of pages specified by the user.  
- **Dynamic Content Handling**: Handles dynamic web content by scrolling through pages to load all items.  
- **Filtered Link Collection**: Excludes non-listing links such as login, recommendations, and booster ads.  
- **Custom Directory and File Management**: Saves collected links in organized directories for easy access.
- **Scraping Links**: Getting item information as the main information is (phone number).

---

## Requirements  

- **Python 3.x**  
- **Firefox Browser**  
- **GeckoDriver**: Required to run the Selenium Firefox WebDriver.

## Setup and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/mihaiapostol14/parser_999_md.git
cd parser_999_md
```

### 2. Create and Activate a Virtual Environment

**Install Python**

If you don't have Python installed, follow [this link](https://www.python.org/downloads/) and download the latest version of Python. Then you can check your version of Python using the command lines below:

```bash
# Create a virtual environment
python -m venv venv  

# Activate the virtual environment
source venv/bin/activate  # Linux/MacOS  
venv\Scripts\activate     # Windows  
```

### 3. Install the Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Setup project configurations
Website where can you [Get User Agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/)

You can use `setup_private.py` or bash code to your preference for creating a `.env` file with private data (user-agent, username, password):

```bash
#!/bin/bash

# Define the path to the config directory and the .env file
CONFIG_DIR="config"
ENV_FILE="$CONFIG_DIR/.env"

# Create the config directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "Creating directory: $CONFIG_DIR"
    mkdir "$CONFIG_DIR"
else
    echo "Directory $CONFIG_DIR already exists."
fi

# Change to the config directory
cd "$CONFIG_DIR" || exit

# Check if the .env file already exists
if [ -f "$ENV_FILE" ]; then
    echo "$ENV_FILE already exists. Overwriting..."
else
    echo "$ENV_FILE does not exist. Creating a new one..."
fi

# Write the data into the .env file
echo "USER_AGENT='user agent'" > "$ENV_FILE"

echo ".env file created successfully with data:"
cat "$ENV_FILE"

 ```