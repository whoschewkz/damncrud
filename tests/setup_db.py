"""
setup_db.py - Script untuk setup database DamnCRUD
Menggunakan damncrud.sql sebagai backup dan sumber data
"""

import mysql.connector
from mysql.connector import Error
import subprocess
import os
import sys

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''  # XAMPP default: empty password
DB_NAME = 'damncrud'  # Match with damncrud.sql

# Path ke SQL file backup
SQL_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'damncrud.sql')

# MySQL binary path (for Windows XAMPP)
XAMPP_MYSQL_PATH = r'C:\xampp\mysql\bin\mysql.exe'


def setup_database_from_sql():
    """Setup database menggunakan damncrud.sql backup file dengan subprocess"""
    try:
        # Verify SQL file exists
        if not os.path.exists(SQL_FILE_PATH):
            print(f"✗ SQL file not found: {SQL_FILE_PATH}")
            print(f"  Fallback: Creating database manually...")
            return setup_database_manual()
        
        print(f"Setting up database from: {SQL_FILE_PATH}")
        print("Loading and executing SQL file...")
        
        # Use mysql command directly to execute SQL file
        mysql_path = r'C:\xampp\mysql\bin\mysql.exe'
        
        if not os.path.exists(mysql_path):
            # Try alternative path
            mysql_path = 'mysql'
        
        # Build command
        cmd = [mysql_path, '-u', DB_USER]
        if DB_PASSWORD:
            cmd.append('-p' + DB_PASSWORD)
        cmd.extend(['-h', DB_HOST])
        
        # Execute SQL file
        try:
            with open(SQL_FILE_PATH, 'r', encoding='utf-8') as sql_file:
                result = subprocess.run(
                    cmd,
                    stdin=sql_file,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            if result.returncode == 0:
                print(f"✓ Database setup from '{os.path.basename(SQL_FILE_PATH)}' completed!")
                return True
            else:
                print(f"  Warning: {result.stderr[:100]}...")
                print(f"  Fallback: Creating database manually...")
                return setup_database_manual()
                
        except FileNotFoundError:
            print(f"  MySQL not found at {mysql_path}")
            print(f"  Fallback: Creating database manually...")
            return setup_database_manual()
        except Exception as e:
            print(f"  Error: {str(e)[:100]}...")
            print(f"  Fallback: Creating database manually...")
            return setup_database_manual()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return setup_database_manual()


def setup_database_manual():
    """Fallback: Setup database dan tables secara manual"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Create database
        print(f"Creating database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.execute(f"USE `{DB_NAME}`")
        connection.commit()
        print(f"✓ Database '{DB_NAME}' ready")
        
        # Create contacts table
        print("Creating 'contacts' table...")
        contacts_table = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(255),
            title VARCHAR(255),
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
        """
        cursor.execute(contacts_table)
        connection.commit()
        print("✓ 'contacts' table created")
        
        # Create users table
        print("Creating 'users' table...")
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id_user INT(2) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci
        """
        cursor.execute(users_table)
        connection.commit()
        print("✓ 'users' table created")
        
        # Insert admin user with hashed password
        print("Setting up admin user...")
        import hashlib
        salt = "XDrBmrW9g2fb"
        password = "nimda666!"
        hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()
        
        cursor.execute(
            "INSERT IGNORE INTO users (username, password) VALUES (%s, %s)",
            ("admin", hashed_pw)
        )
        connection.commit()
        print("✓ Admin user 'admin/nimda666!' setup")
        
        # Insert sample test data (fewer data untuk faster tests)
        print("Inserting sample test data...")
        test_contacts = [
            ('John Doe', 'john.doe@example.com', '08123456789', 'Software Engineer'),
            ('Jane Smith', 'jane.smith@example.com', '08987654321', 'Product Manager'),
            ('Bob Johnson', 'bob.johnson@example.com', '08111111111', 'QA Engineer'),
            ('Alice Brown', 'alice.brown@example.com', '08222222222', 'UI/UX Designer'),
            ('Charlie Wilson', 'charlie.wilson@example.com', '08333333333', 'DevOps Engineer'),
        ]
        
        for contact in test_contacts:
            cursor.execute(
                "INSERT INTO contacts (name, email, phone, title) VALUES (%s, %s, %s, %s)",
                contact
            )
        connection.commit()
        print(f"✓ {len(test_contacts)} sample contacts inserted")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error during manual database setup: {e}")
        return False


def verify_database():
    """Verify database setup"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n✓ Database '{DB_NAME}' contains {len(tables)} table(s):")
        for table in tables:
            print(f"  └─ {table[0]}")
        
        # Check users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT username FROM users LIMIT 1")
        user_result = cursor.fetchone()
        user_info = f"{user_count} user(s)"
        if user_result:
            user_info += f" - Admin: '{user_result[0]}'"
        print(f"\n✓ Users: {user_info}")
        
        # Check contacts
        cursor.execute("SELECT COUNT(*) FROM contacts")
        contact_count = cursor.fetchone()[0]
        print(f"✓ Contacts: {contact_count} record(s)")
        
        cursor.close()
        connection.close()
        
        print("\n✓ Database verification completed successfully!")
        return True
        
    except Error as e:
        print(f"✗ Error during verification: {e}")
        return False


def reset_database_for_tests():
    """Reset database dengan minimal data untuk testing"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        
        # Clear existing contacts
        print("Resetting database for testing...")
        cursor.execute("TRUNCATE TABLE contacts")
        
        # Insert minimal test data
        test_contacts = [
            ('John Doe', 'john.doe@email.com', '08123456789', 'Software Engineer'),
            ('Jane Smith', 'jane.smith@email.com', '08987654321', 'Product Manager'),
            ('Bob Johnson', 'bob.johnson@email.com', '08111111111', 'QA Engineer'),
        ]
        
        for contact in test_contacts:
            cursor.execute(
                "INSERT INTO contacts (name, email, phone, title) VALUES (%s, %s, %s, %s)",
                contact
            )
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print(f"✓ Database reset with {len(test_contacts)} test contacts")
        return True
        
    except Error as e:
        print(f"✗ Error during database reset: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("DamnCRUD Database Setup")
    print("=" * 50)
    print()
    
    # Setup database from SQL file or fallback to manual
    if setup_database_from_sql():
        # Verify setup
        verify_database()
        print("\n" + "=" * 50)
        print("✓ DamnCRUD Database Ready!")
        print("=" * 50)
    else:
        print("\n✗ Database setup failed!")
        sys.exit(1)
