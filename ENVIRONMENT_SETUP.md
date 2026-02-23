# DamnCRUD Test Automation Environment Setup

## Environment Configuration

### Database Configuration

**File:** `tests/conftest.py`

```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'root123'
DB_NAME = 'badcrud'
```

**Update jika menggunakan:**
- Remote database: ubah `DB_HOST`
- Different credentials: ubah `DB_USER` dan `DB_PASSWORD`
- Different port: ubah port di connection string

### Application Configuration

**File:** `tests/conftest.py`

```python
BASE_URL = 'http://localhost/DamnCRUD'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'nimda666!'
IMPLICIT_WAIT = 10
HEADLESS = False  # Set to True untuk CI/CD
```

### Selenium Configuration

**Browser Options:**
```python
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

**Headless Mode (untuk CI/CD):**
```python
if HEADLESS:
    chrome_options.add_argument("--headless")
```

## Platform-Specific Setup

### Windows Setup

#### 1. Install Python
```powershell
# Download dari https://www.python.org/downloads/
# Pastikan "Add Python to PATH" di-check saat installation

# Verify
python --version
```

#### 2. Install XAMPP

```powershell
# Download dari https://www.apachefriends.org/
# Run installer
# Start Apache dan MySQL dari XAMPP Control Panel
```

#### 3. Clone Repository

```powershell
cd C:\xampp\htdocs
git clone https://github.com/yourusername/DamnCRUD.git
cd DamnCRUD
```

#### 4. Install Dependencies

```powershell
# Create virtual environment (optional tapi recommended)
python -m venv venv
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

#### 5. Setup Database

```powershell
python tests/setup_db.py
```

#### 6. Run Tests

```powershell
# Verify XAMPP running (Apache + MySQL)

# Run tests
pytest tests/ -v -n auto

# atau
python -m pytest tests/ -v -n auto
```

### Linux Setup

#### 1. Install Python & Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y mysql-server apache2 php php-mysql
```

#### 2. Clone Repository

```bash
cd /var/www/html
git clone https://github.com/yourusername/DamnCRUD.git
cd DamnCRUD
```

#### 3. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Configure Apache

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

#### 5. Setup Database

```bash
sudo mysql -u root
> CREATE DATABASE badcrud;
> exit;

python tests/setup_db.py
```

#### 6. Run Tests

```bash
pytest tests/ -v -n auto
```

### macOS Setup

#### 1. Install Dependencies

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install packages
brew install python mysql apache2 php
```

#### 2. Clone Repository

```bash
cd ~/Development  # atau folder pilihan Anda
git clone https://github.com/yourusername/DamnCRUD.git
cd DamnCRUD
```

#### 3. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Start Services

```bash
# MySQL
brew services start mysql

# Apache
sudo apachectl start
```

#### 5. Setup Database

```bash
python tests/setup_db.py
```

#### 6. Run Tests

```bash
pytest tests/ -v -n auto
```

## Docker Setup (Alternative)

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    image: php:8.1-apache
    ports:
      - "80:80"
    volumes:
      - ./:/var/www/html
    environment:
      - MYSQL_HOST=db
      - MYSQL_USER=root
      - MYSQL_PASSWORD=root123

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: badcrud
    ports:
      - "3306:3306"
    volumes:
      - ./db:/docker-entrypoint-initdb.d
```

### Run with Docker

```bash
# Start containers
docker-compose up -d

# Wait untuk services to be ready
sleep 10

# Run tests
docker exec -it damncrud_web pip install -r requirements.txt
docker exec -it damncrud_web python tests/setup_db.py
docker exec -it damncrud_web pytest tests/ -v -n auto

# Cleanup
docker-compose down
```

## Continuous Integration Setup

### GitHub Secrets (jika menggunakan credentials)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   ```
   DB_HOST = localhost
   DB_USER = root
   DB_PASSWORD = root123
   ```

### GitHub Actions Configuration

File: `.github/workflows/ci_cd.yml` sudah di-setup dengan:
- ✅ MySQL service
- ✅ Apache configuration
- ✅ Python dependencies
- ✅ Parallel test execution
- ✅ Report generation

## Testing Environment Variables

### Local Development

Buat file `.env` (tidak di-commit):
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root123
BASE_URL=http://localhost/DamnCRUD
HEADLESS=False
```

Load dengan:
```python
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv('DB_HOST', 'localhost')
```

### CI/CD Environment

Set di GitHub Actions workflow:
```yaml
env:
  DB_HOST: localhost
  DB_USER: root
  DB_PASSWORD: root123
  HEADLESS: true
```

## Verification Checklist

Sebelum menjalankan tests, verify:

- [ ] Python installed (`python --version` ≥ 3.9)
- [ ] MySQL running (`mysql -u root -proot123 -e "SELECT 1"`)
- [ ] Apache running (`curl http://localhost` returns something)
- [ ] Database created (`mysql -u root -proot123 badcrud -e "SHOW TABLES"`)
- [ ] Application accessible (`curl http://localhost/DamnCRUD/login.php`)
- [ ] Chrome/Chromium installed (`google-chrome --version` atau `chromium-browser --version`)
- [ ] Python dependencies installed (`pip list | grep selenium`)

### Verification Script

```bash
#!/bin/bash

echo "DamnCRUD Environment Verification"
echo "=================================="

# Check Python
python --version || echo "❌ Python not found"

# Check MySQL
mysql -u root -proot123 -e "SELECT 1" >/dev/null 2>&1 && echo "✓ MySQL running" || echo "❌ MySQL not running"

# Check Apache
curl -s http://localhost > /dev/null && echo "✓ Apache running" || echo "❌ Apache not running"

# Check Database
mysql -u root -proot123 badcrud -e "SHOW TABLES" >/dev/null 2>&1 && echo "✓ Database exists" || echo "❌ Database not found"

# Check Application
curl -s http://localhost/DamnCRUD/login.php | grep -q "Damn, sign in" && echo "✓ Application running" || echo "❌ Application not accessible"

# Check Chrome
which google-chrome > /dev/null 2>&1 && echo "✓ Chrome found" || echo "❌ Chrome not found"

# Check Python packages
pip show selenium > /dev/null 2>&1 && echo "✓ Selenium installed" || echo "❌ Selenium not installed"
pip show pytest > /dev/null 2>&1 && echo "✓ Pytest installed" || echo "❌ Pytest not installed"

echo "=================================="
echo "Verification complete"
```

## Troubleshooting Environment Setup

### Problem: Python not found

**Solutions:**
1. Verify installation: `which python3` atau `where python` (Windows)
2. Add to PATH:
   - Windows: Control Panel → System → Environment Variables
   - Linux/Mac: Update `.bashrc` atau `.zshrc`

### Problem: MySQL connection failed

**Solutions:**
1. Check service running:
   ```bash
   # Linux
   sudo systemctl status mysql
   
   # macOS
   brew services list
   
   # Windows - XAMPP Control Panel
   ```

2. Test connection:
   ```bash
   mysql -h localhost -u root -proot123 -e "SELECT 1"
   ```

3. Reset MySQL:
   ```bash
   # Linux
   sudo systemctl restart mysql
   
   # XAMPP - restart dari control panel
   ```

### Problem: Apache not running

**Solutions:**
1. Check service:
   ```bash
   # Linux
   sudo systemctl status apache2
   sudo systemctl start apache2
   ```

2. XAMPP - click "Start" untuk Apache

3. Verify:
   ```bash
   curl http://localhost
   ```

### Problem: Chrome not found

**Solutions:**
1. Install Chrome:
   ```bash
   # Ubuntu
   sudo apt-get install chromium-browser
   
   # macOS
   brew install --cask google-chrome
   ```

2. Install webdriver-manager:
   ```bash
   pip install webdriver-manager
   ```

3. Update conftest.py:
   ```python
   from webdriver_manager.chrome import ChromeDriverManager
   driver = webdriver.Chrome(ChromeDriverManager().install())
   ```

## Performance Optimization

### For Faster Tests

1. **Use Headless Mode:**
   ```python
   HEADLESS = True  # In conftest.py
   ```

2. **Reduce Wait Times (if app is fast):**
   ```python
   IMPLICIT_WAIT = 5  # Change from 10
   ```

3. **Parallel Execution:**
   ```bash
   pytest tests/ -n 8  # Use more cores
   ```

### For Better Stability

1. **Increase Waits (if app is slow):**
   ```python
   IMPLICIT_WAIT = 15  # Increase from 10
   ```

2. **Add Server Health Check:**
   ```python
   import requests
   response = requests.get(f"{BASE_URL}/login.php")
   assert response.status_code == 200
   ```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | localhost | MySQL host |
| `DB_USER` | root | MySQL user |
| `DB_PASSWORD` | root123 | MySQL password |
| `DB_NAME` | badcrud | Database name |
| `BASE_URL` | http://localhost/DamnCRUD | Application URL |
| `ADMIN_USERNAME` | admin | Admin user |
| `ADMIN_PASSWORD` | nimda666! | Admin password |
| `IMPLICIT_WAIT` | 10 | Selenium wait (seconds) |
| `HEADLESS` | False | Browser headless mode |

## Post-Setup Verification

Setelah setup selesai, jalankan:

```bash
# Quick test
pytest tests/test_damncrud.py::TestDamnCRUDRead::test_tc003_view_contact_list_on_dashboard -v

# Full test suite
pytest tests/ -v

# With report
pytest tests/ -v --html=tests/reports/report.html
```

Jika semua tests PASS ✅, environment setup berhasil!

---

**Last Updated:** 2024
**Status:** Ready for Testing ✅
