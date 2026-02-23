# DamnCRUD - Automated Testing Guide

## Table of Contents
1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [Running Tests Locally](#running-tests-locally)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Test Architecture](#test-architecture)
6. [Troubleshooting](#troubleshooting)

---

## Overview

DamnCRUD Testing Suite menyediakan:
- ✅ **5 Automated Test Cases** menggunakan Python + Selenium
- ✅ **Parallel Execution** dengan Pytest-xdist
- ✅ **CI/CD Pipeline** dengan GitHub Actions
- ✅ **HTML Reports** untuk hasil testing
- ✅ **Database Reset** otomatis untuk setiap test

### Test Cases yang Diotomasi

| TC | Deskripsi | Status |
|---|---|---|
| TC003 | View Contact List on Dashboard | ✅ Read |
| TC004 | Create New Contact | ✅ Create |
| TC006 | Update Existing Contact | ✅ Update |
| TC007 | Delete Contact | ✅ Delete |
| TC008 | Access Protected Page Without Login | ✅ Security |

---

## Environment Setup

### Prerequisites
- **OS**: Windows 10+ / macOS / Linux
- **Python**: 3.9 atau lebih baru
- **Apache**: XAMPP atau server lokal lainnya
- **MySQL**: 5.7 atau lebih baru
- **Chrome/Chromium**: Browser untuk Selenium

### Step 1: Install Python Dependencies

```bash
# Clone atau navigate ke folder DamnCRUD
cd DamnCRUD

# Install dependencies
pip install -r requirements.txt
```

**Dependencies yang akan diinstall:**
- `selenium` - Web automation framework
- `pytest` - Testing framework
- `pytest-xdist` - Parallel execution plugin
- `pytest-html` - HTML report generation
- `mysql-connector-python` - MySQL database driver

### Step 2: Setup Database

```bash
# Run database setup script
python tests/setup_db.py
```

**Database akan di-setup dengan:**
- Database: `badcrud`
- User: `admin` / Password: `nimda666!`
- Test data: 5 sample contacts

### Step 3: Start Apache & MySQL

#### Using XAMPP
```bash
# Windows
xampp\xampp-control.exe
# Start Apache dan MySQL

# Linux/Mac
sudo /opt/lampp/lampp start
```

#### atau Verify Database Connection
```bash
mysql -h localhost -u root -proot123 badcrud -e "SELECT * FROM contacts LIMIT 1;"
```

### Step 4: Verify Application is Running

Buka browser dan akses: `http://localhost/DamnCRUD/login.php`

Anda seharusnya melihat halaman login dengan username dan password fields.

---

## Running Tests Locally

### Option 1: Run All Tests (Recommended)

```bash
# Menggunakan script helper (Linux/Mac)
chmod +x run_tests.sh
./run_tests.sh all

# Atau direct dengan pytest
pytest tests/ -v -n auto
```

### Option 2: Run Specific Test Type

```bash
# Run CREATE tests only
pytest tests/ -v -k "test_tc004"

# Run READ tests
pytest tests/ -v -k "test_tc003 or test_tc008"

# Run UPDATE tests
pytest tests/ -v -k "test_tc006"

# Run DELETE tests
pytest tests/ -v -k "test_tc007"
```

### Option 3: Run with Serial Execution (Debugging)

```bash
# Single worker (tidak parallel)
pytest tests/ -v -n 1
```

### Option 4: Generate HTML Report

```bash
# Generate test report
pytest tests/ -v -n auto --html=tests/reports/report.html --self-contained-html

# Report akan di-generate di: tests/reports/report.html
```

### Option 5: Run Specific Test File

```bash
# Run only test_damncrud.py
pytest tests/test_damncrud.py -v -n auto

# Run specific test class
pytest tests/test_damncrud.py::TestDamnCRUDCreate -v

# Run specific test method
pytest tests/test_damncrud.py::TestDamnCRUDCreate::test_tc004_create_new_contact -v
```

### Running Tests with Different Parallelization

```bash
# Auto-detect CPU cores (recommended)
pytest tests/ -n auto

# Specify number of workers
pytest tests/ -n 4      # Use 4 workers

# Serial execution (no parallelization)
pytest tests/ -v        # Default without -n flag
```

### Available Run Commands (run_tests.sh)

```bash
./run_tests.sh all          # Run semua tests
./run_tests.sh parallel     # Run dengan parallelization
./run_tests.sh serial       # Run serial
./run_tests.sh create       # Create tests only
./run_tests.sh read         # Read tests only
./run_tests.sh update       # Update tests only
./run_tests.sh delete       # Delete tests only
./run_tests.sh integration  # Integration tests
./run_tests.sh report       # Generate HTML report
./run_tests.sh markers      # Show markers
./run_tests.sh collect      # Collect tests only
./run_tests.sh help         # Show help
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

File: `.github/workflows/ci_cd.yml`

#### Workflow Triggers
- **Push** ke branch: `main`, `master`, `develop`
- **Pull Request** ke branch: `main`, `master`, `develop`
- **Schedule**: Setiap hari jam 2 pagi UTC

#### Pipeline Stages

```
├── Test Job
│   ├── Checkout code
│   ├── Setup Python 3.11
│   ├── Install system dependencies
│   ├── Configure Apache
│   ├── Setup MySQL
│   ├── Install Python dependencies
│   ├── Run Pytest (parallel)
│   ├── Generate reports
│   └── Upload artifacts
│
└── Code Quality Job
    ├── Flake8 lint
    └── Pylint check
```

#### Pipeline Features
- ✅ **Parallel Test Execution** menggunakan pytest-xdist
- ✅ **MySQL Service** di Docker container
- ✅ **Apache Setup** otomatis
- ✅ **HTML Report** generation
- ✅ **Artifact Upload** untuk test reports
- ✅ **Email Notifications** (configurable)

#### Viewing Results

1. Go to GitHub Repository
2. Click **Actions** tab
3. Select workflow run
4. View job logs dan artifacts

#### Download Artifacts

```bash
# Artifacts tersedia untuk download di GitHub Actions UI:
- pytest-html-report (report.html)
- pytest-junit-report (junit.xml)
```

---

## Test Architecture

### Folder Structure

```
DamnCRUD/
├── tests/
│   ├── conftest.py           # Pytest fixtures & setup
│   ├── test_damncrud.py      # Main test cases
│   ├── setup_db.py           # Database setup script
│   └── reports/              # Test reports (generated)
├── .github/
│   └── workflows/
│       └── ci_cd.yml         # GitHub Actions workflow
├── requirements.txt          # Python dependencies
├── pytest.ini                # Pytest configuration
├── run_tests.sh              # Test runner script
├── TEST_CASE.md              # Test case documentation
└── TESTING_GUIDE.md          # This file
```

### Fixtures (conftest.py)

#### `browser` Fixture
- Initializes Chrome WebDriver
- Maximizes window
- Implicit wait: 10 seconds
- Quits driver after test

Usage:
```python
def test_example(browser):
    browser.get("http://localhost/DamnCRUD/login.php")
    # Test code here
```

#### `authenticated_browser` Fixture
- Extends `browser` fixture
- Automatically logs in as admin
- Ready for protected page testing

Usage:
```python
def test_example(authenticated_browser):
    # Already logged in, dapat langsung test
    authenticated_browser.get("http://localhost/DamnCRUD/index.php")
```

#### `db_connection` Fixture
- Creates MySQL connection
- Automatically closes after test

Usage:
```python
def test_example(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM contacts")
```

#### `reset_database` Autouse Fixture
- Runs before setiap test
- Resets contacts table
- Inserts test data

### Helper Classes

#### LoginHelper
```python
from conftest import LoginHelper

# Usage dalam test
LoginHelper.login(driver, username="admin", password="nimda666!")
```

### Test Classes Organization

```python
class TestDamnCRUDRead:      # READ operations (TC003, TC008)
class TestDamnCRUDCreate:    # CREATE operations (TC004)
class TestDamnCRUDUpdate:    # UPDATE operations (TC006)
class TestDamnCRUDDelete:    # DELETE operations (TC007)
class TestCRUDIntegration:   # Integration tests
```

---

## Parallel Execution Details

### Pytest-xdist Configuration

File: `pytest.ini`

```ini
addopts = 
    -n auto              # Auto-detect CPU cores
```

### Parallelization Strategy

```
Available CPUs: 4
Tests: 5
Distribution: pytest-xdist akan auto-distribute

Example execution time:
- Serial: ~50 seconds (5 tests × 10 seconds)
- Parallel (4 cores): ~15-20 seconds
```

### Managing Test Isolation

Setiap test berjalan independen:
- Database di-reset sebelum test (fixture `reset_database`)
- Browser session baru untuk setiap test
- No shared state antar tests

### Controlling Parallelization

```bash
# Auto (recommended)
pytest -n auto

# Specific number
pytest -n 2

# Disable parallelization
pytest -v          # No -n flag

# Show parallelization info
pytest -v --dist=loadfile
```

---

## Troubleshooting

### Problem: "Cannot find Chrome WebDriver"

**Solution:**
```bash
# Install webdriver-manager
pip install webdriver-manager

# Update conftest.py to use it
```

### Problem: "Connection refused" untuk database

**Solutions:**
1. Verifikasi MySQL running:
   ```bash
   mysql -u root -proot123 -e "SELECT 1"
   ```

2. Setup database:
   ```bash
   python tests/setup_db.py
   ```

3. Cek credentials di `conftest.py`:
   ```python
   DB_HOST = 'localhost'       # atau 127.0.0.1
   DB_USER = 'root'
   DB_PASSWORD = 'root123'
   DB_NAME = 'badcrud'
   ```

### Problem: "Connection refused" untuk Apache

**Solutions:**
1. Start Apache:
   ```bash
   # XAMPP
   sudo /opt/lampp/lampp start
   
   # atau manual
   sudo systemctl start apache2
   ```

2. Verify Application:
   ```bash
   curl http://localhost/DamnCRUD/login.php
   ```

### Problem: Tests timeout

**Solutions:**
1. Increase timeout di `pytest.ini`:
   ```ini
   timeout = 600  # 10 minutes
   ```

2. Run serially instead:
   ```bash
   pytest tests/ -v -n 1
   ```

3. Run with debug:
   ```bash
   pytest tests/ -v -s --capture=no
   ```

### Problem: "Flaky" tests (intermittent failures)

**Solutions:**
1. Verify application responsiveness:
   ```bash
   for i in {1..5}; do curl http://localhost/DamnCRUD/login.php; done
   ```

2. Increase implicit wait di `conftest.py`:
   ```python
   driver.implicitly_wait(15)  # Changed from 10
   ```

3. Add explicit waits di test:
   ```python
   WebDriverWait(driver, 15).until(
       EC.presence_of_element_located((By.ID, "name"))
   )
   ```

### Problem: Database state mismatch

**Solutions:**
1. Manually reset database:
   ```bash
   python tests/setup_db.py
   ```

2. Delete pytest cache:
   ```bash
   rm -rf .pytest_cache
   ```

3. Re-run tests:
   ```bash
   pytest tests/ -v --cache-clear
   ```

---

## Performance Optimization

### Test Execution Time

**Current Configuration:**
- Single test average: ~10-15 seconds
- 5 tests parallel: ~20-25 seconds
- 5 tests serial: ~50-75 seconds

**Optimization Tips:**
1. Use `authenticated_browser` fixture untuk avoid login repetition
2. Reduce implicit wait untuk fast applications
3. Use headless mode di CI/CD:
   ```python
   chrome_options.add_argument("--headless")
   ```

### Memory Usage

**Per test instance:**
- Chrome WebDriver: ~100-150 MB
- MySQL connection: ~5-10 MB
- Python process: ~20-30 MB

---

## Best Practices

1. ✅ Always use fixtures untuk setup/teardown
2. ✅ Use explicit waits instead of sleep()
3. ✅ Reset database sebelum test
4. ✅ Use descriptive test names
5. ✅ Group related tests dalam classes
6. ✅ Document test objectives
7. ✅ Use markers untuk test classification
8. ✅ Generate reports untuk CI/CD
9. ✅ Monitor pipeline performance
10. ✅ Update tests saat aplikasi berubah

---

## Support & Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Selenium Documentation**: https://selenium-python.readthedocs.io/
- **pytest-xdist**: https://pytest-xdist.readthedocs.io/
- **GitHub Actions**: https://docs.github.com/en/actions

---

## Last Updated
- Date: 2024
- Version: 1.0
- Status: Production Ready ✅
