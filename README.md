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
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup project configurations
Website where can you [Get User Agent](https://www.whatismybrowser.com/detect/what-is-my-user-agent/)

You can use `setup_private.py` or `setup_private.sh` to your preference for creating a `.env` file with private data (user-agent, username, password):


## Author
[Mihai Apostol](https://github.com/mihaiapostol14)