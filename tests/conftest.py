"""
conftest.py - Pytest fixtures untuk setup dan teardown test environment
"""
import pytest
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

# Detect if running in GitHub Actions
IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'

# Database Configuration
DB_HOST = '127.0.0.1' if IS_GITHUB_ACTIONS else 'localhost'  # GitHub Actions uses 127.0.0.1
DB_USER = 'root'
DB_PASSWORD = ''  # XAMPP default: empty password
DB_NAME = 'damncrud'  # Match with damncrud.sql

# Application Configuration
APP_HOST = '127.0.0.1' if IS_GITHUB_ACTIONS else 'localhost'
BASE_URL = f'http://{APP_HOST}/DamnCRUD'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nimda666!'

# Selenium Configuration
IMPLICIT_WAIT = 10
HEADLESS = IS_GITHUB_ACTIONS  # Automatically enable headless mode in GitHub Actions

print(f"[Pytest Config] Running in GitHub Actions: {IS_GITHUB_ACTIONS}")
print(f"[Pytest Config] Database Host: {DB_HOST}")
print(f"[Pytest Config] Base URL: {BASE_URL}")
print(f"[Pytest Config] Headless Mode: {HEADLESS}")


def get_db_connection():
    """Create database connection"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None


@pytest.fixture(scope="function")
def browser():
    """
    Fixture untuk initialize dan teardown Chrome WebDriver
    """
    chrome_options = Options()

    if HEADLESS:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # ===== FIX UNTUK GITHUB ACTIONS =====
    if IS_GITHUB_ACTIONS:
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        # Lokal (XAMPP / Windows)
        driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(IMPLICIT_WAIT)

    # maximize_window tidak diperlukan di headless
    if not HEADLESS:
        driver.maximize_window()

    yield driver

    driver.quit()

@pytest.fixture(scope="function")
def db_connection():
    """
    Fixture untuk database connection
    """
    connection = get_db_connection()
    
    yield connection
    
    # Cleanup - Close connection
    if connection and connection.is_connected():
        connection.close()


@pytest.fixture(autouse=True)
def reset_database():
    """
    Fixture untuk reset database sebelum setiap test
    Dengan locking untuk prevent race condition di parallel execution
    """
    import time
    import os
    
    # Lock file untuk prevent concurrent database resets
    lock_file = os.path.join(os.path.dirname(__file__), '.db_lock')
    
    # Wait untuk lock (dengan timeout)
    max_wait = 10
    wait_time = 0
    while os.path.exists(lock_file) and wait_time < max_wait:
        time.sleep(0.5)
        wait_time += 0.5
    
    # Create lock
    try:
        with open(lock_file, 'w') as f:
            f.write('locked')
    except:
        pass
    
    try:
        # Reset database - delete semua data dari contacts table
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                # Reset auto increment dan clear data
                cursor.execute("DELETE FROM contacts")
                
                # Insert test data
                insert_query = """
                INSERT INTO contacts (name, email, phone, title, created) 
                VALUES (%s, %s, %s, %s, %s)
                """
                test_data = [
                    ('John Doe', 'john.doe@email.com', '08123456789', 'Software Engineer', '2023-01-15 10:00:00'),
                    ('Jane Smith', 'jane.smith@email.com', '08987654321', 'Product Manager', '2023-01-16 11:00:00'),
                    ('Bob Johnson', 'bob.johnson@email.com', '08111111111', 'QA Engineer', '2023-01-17 12:00:00'),
                ]
                
                for data in test_data:
                    cursor.execute(insert_query, data)
                
                connection.commit()
            except Exception as e:
                print(f"Error resetting database: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        
        time.sleep(0.5)  # Extra buffer time
    finally:
        # Release lock
        try:
            if os.path.exists(lock_file):
                os.remove(lock_file)
        except:
            pass
    
    yield
    
    # Cleanup after test jika diperlukan


class LoginHelper:
    """Helper class untuk login operations"""
    
    @staticmethod
    def login(driver, username=ADMIN_USERNAME, password=ADMIN_PASSWORD):
        """Login dengan kredensial yang diberikan"""
        driver.get(f"{BASE_URL}/login.php")
        
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("id", "inputUsername"))
        )
        password_field = driver.find_element("id", "inputPassword")
        submit_button = driver.find_element("xpath", "//button[@type='submit']")
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()
        
        # Wait for redirect to dashboard
        WebDriverWait(driver, 10).until(
            EC.url_contains("/index.php")
        )
        time.sleep(1)


@pytest.fixture
def authenticated_browser(browser):
    """
    Fixture untuk browser yang sudah login
    """
    LoginHelper.login(browser)
    yield browser
