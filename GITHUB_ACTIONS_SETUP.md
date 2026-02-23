# Setup CI/CD dengan GitHub Actions - Panduan Lengkap

Panduan ini menjelaskan langkah demi langkah cara menambahkan project DamnCRUD ke GitHub dan mengkonfigurasi CI/CD Pipeline menggunakan GitHub Actions.

---

## ⏱️ Perkiraan Waktu Total: 20-30 menit

---

## BAGIAN 1: Persiapan di GitHub (5 menit)

### Step 1.1: Buat Akun GitHub (Jika belum punya)
- Kunjungi https://github.com
- Klik "Sign up"
- Isi form registrasi dengan email, password, dan username
- Verifikasi email Anda

### Step 1.2: Buat Repository Baru
1. Setelah login ke GitHub, klik **"+"** di top-right → **"New repository"**
2. Isi form:
   - **Repository name**: `damncrud` (atau nama lainnya)
   - **Description**: `Automated CRUD Testing Suite - Functional Testing dengan Python & Selenium`
   - **Visibility**: Pilih **"Public"** (agar CI/CD logs bisa dilihat) atau **"Private"**
   - **Initialize repository**: Jangan centang apa-apa (akan push dari lokal)
3. Klik **"Create repository"**
4. Repository akan otomatis mengarahkan Anda ke halaman setup

### Step 1.3: Copy URL Repository
- Di halaman repository, klik tombol hijau **"< > Code"**
- Pilih tab **"HTTPS"** (rekomendasi untuk pemula)
- Copy URL yang terlihat: `https://github.com/your-username/damncrud.git`
- Simpan URL ini, akan digunakan di langkah selanjutnya

---

## BAGIAN 2: Setup Git di Lokal Machine (5 menit)

### Step 2.1: Install Git (Jika belum terinstall)
1. Unduh dari https://git-scm.com/download/win
2. Jalankan installer dan ikuti langkah default
3. Verifikasi instalasi dengan buka PowerShell dan jalankan:
   ```powershell
   git --version
   ```
   Output yang diharapkan: `git version 2.x.x...`

### Step 2.2: Konfigurasi Git Identity
Buka PowerShell dan jalankan perintah berikut (ubah dengan data Anda):

```powershell
git config --global user.name "Nama Anda"
git config --global user.email "email@example.com"
```

**Contoh:**
```powershell
git config --global user.name "Budi Santoso"
git config --global user.email "budi@example.com"
```

### Step 2.3: Setup Personal Access Token (PAT)
Untuk push ke GitHub tanpa input password setiap kali:

1. Di GitHub, klik foto profil (top-right) → **"Settings"**
2. Di sidebar kiri, scroll ke bawah dan klik **"Developer settings"**
3. Klik **"Personal access tokens"** → **"Tokens (classic)"**
4. Klik **"Generate new token"** → **"Generate new token (classic)"**
5. Isi form:
   - **Token name**: `damncrud-ci-cd`
   - **Expiration**: Pilih **"90 days"** (atau sesuai preferensi)
   - **Scopes**: Centang kotak `repo` (full control of private repositories)
6. Klik **"Generate token"** (hijau)
7. **PENTING**: Copy token yang ditampilkan dan simpan di tempat aman (hanya ditampilkan sekali!)

### Step 2.4: Simpan Credential di Git Manager (Windows)
1. Buka **Credential Manager**:
   - Tekan `Win + R`
   - Ketik: `control /name Microsoft.CredentialManager`
   - Tekan Enter
2. Klik **"Windows Credentials"**
3. Klik **"Add a generic credential"**
4. Isi:
   - **Internet or network address**: `https://github.com`
   - **User name**: `your-username`
   - **Password**: `paste token yang sudah di-copy`
5. Klik **"OK"**

---

## BAGIAN 3: Inisialisasi Repository Lokal (5 menit)

### Step 3.1: Navigasi ke Folder Project
Buka PowerShell dan navigasi ke folder DamnCRUD:

```powershell
cd C:\xampp\htdocs\DamnCRUD
```

**Verifikasi** Anda di folder yang benar dengan melihat file-file ada:
```powershell
ls
```

Hasilnya harus menampilkan: `index.php`, `login.php`, `tests/`, `db/`, `.github/` dan file lainnya

### Step 3.2: Inisialisasi Git Repository
```powershell
git init
```

Output: `Initialized empty Git repository in C:\xampp\htdocs\DamnCRUD\.git/`

### Step 3.3: Tambahkan Remote URL
Ganti `your-username/your-repo` dengan URL yang di-copy di Step 1.3:

```powershell
git remote add origin https://github.com/your-username/damncrud.git
```

**Verifikasi:**
```powershell
git remote -v
```

Output harus menampilkan:
```
origin  https://github.com/your-username/damncrud.git (fetch)
origin  https://github.com/your-username/damncrud.git (push)
```

### Step 3.4: Buat Branch Main (Default)
```powershell
git branch -M main
```

---

## BAGIAN 4: Persiapan File Lokal (5 menit)

### Step 4.1: Verifikasi Struktur File
Pastikan file-file penting sudah ada:

**File yang HARUS ada:**
- ✅ `tests/test_damncrud.py` - Test automation script
- ✅ `tests/conftest.py` - Pytest configuration & fixtures
- ✅ `tests/setup_db.py` - Database setup script
- ✅ `db/damncrud.sql` - Database schema
- ✅ `.github/workflows/ci_cd.yml` - GitHub Actions workflow
- ✅ `requirements.txt` - Python dependencies
- ✅ `functions.php` - Updated dengan credentials benar
- ✅ `pytest.ini` - Pytest config

Jika ada file yang hilang: [Hubungi untuk penjelasan lebih lanjut]

### Step 4.2: Verifikasi requirements.txt
Buka file `requirements.txt` dan pastikan isinya:

```
selenium==4.15.2
pytest==7.4.3
pytest-html==4.1.1
pytest-timeout==2.1.0
pytest-xdist==3.5.0
mysql-connector-python==8.2.0
webdriver-manager==4.0.1
```

Jika belum ada, jalankan:
```powershell
pip freeze > requirements.txt
```

### Step 4.3: Update GitHub Actions Workflow
File: `.github/workflows/ci_cd.yml` harus menggunakan credentials yang benar.

Buka file dan verifikasi bagian `services.mysql.env`:

**BENAR (untuk damncrud database):**
```yaml
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: ''          # Empty password
          MYSQL_DATABASE: damncrud          # Database name
```

**JIKA MASIH MENGGUNAKAN LAMA, UPDATE MENJADI:**

Bagian yang perlu di-update:
1. Line dengan `MYSQL_ROOT_PASSWORD` → ubah ke empty string: `''`
2. Line dengan `MYSQL_DATABASE` → ubah ke: `damncrud`
3. Command: `mysql ... -proot123 badcrud` → ubah ke: `mysql ... -p damncrud`

---

## BAGIAN 5: Commit dan Push ke GitHub (5 menit)

### Step 5.1: Check Status Perubahan
```powershell
git status
```

Output akan menampilkan daftar file yang berubah (20-30 file):
```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .github/
        tests/
        ...
```

### Step 5.2: Tambahkan Semua File
```powershell
git add .
```

### Step 5.3: Commit Perubahan
```powershell
git commit -m "Initial commit: DamnCRUD dengan automated testing suite dan CI/CD pipeline"
```

Output menampilkan jumlah file yang di-commit:
```
[main (root-commit) abc1234] Initial commit...
 30 files changed, 5000 insertions(+)
 ...
```

### Step 5.4: Push ke GitHub
```powershell
git push -u origin main
```

**First time push** mungkin diminta login:
- **Username**: Username GitHub Anda
- **Password**: Gunakan Personal Access Token (bukan password akun GitHub)

Output yang diharapkan:
```
Enumerating objects: 30, done.
Counting objects: 100% (30/30), done.
Compressing objects: 100% (25/25), done.
Writing objects: 100% (30/30)...
To https://github.com/your-username/damncrud.git
 * [new branch]      main -> main
Branch 'main' is tracked by 'origin/main'.
```

---

## BAGIAN 6: Verifikasi di GitHub (2 menit)

### Step 6.1: Refresh Halaman Repository
- Buka GitHub di browser
- Navigasi ke repository Anda
- Refresh halaman (F5)

Anda seharusnya melihat:
- ✅ Semua file ada di repository
- ✅ `.github/workflows/` folder terlihat
- ✅ README.md ditampilkan

### Step 6.2: Verifikasi GitHub Actions Workflow
1. Klik tab **"Actions"** di repository Anda
2. Di sidebar kiri, seharusnya melihat workflow: **"DamnCRUD - Functional Testing CI/CD Pipeline"**
3. Di sebelah kanan, klik workflow ini

---

## BAGIAN 7: Menjalankan CI/CD Pipeline Pertama Kali

### Step 7.1: Trigger Pipeline Secara Manual
**Opsi A: Trigger via GitHub UI**
1. Di tab **"Actions"**, klik workflow **"DamnCRUD - Functional Testing CI/CD Pipeline"**
2. Klik tombol **"Run workflow"** (berwarna abu-abu)
3. Pilih **"Run workflow"** dari dropdown

**Opsi B: Trigger via Commit**
Push commit baru ke repository:
```powershell
git add .
git commit -m "Trigger CI/CD pipeline"
git push
```

### Step 7.2: Monitor Jalannya Pipeline
1. Di GitHub, tab **"Actions"** → workflow yang sedang berjalan ditampilkan dengan status kuning 🟡
2. Klik workflow run untuk melihat detail
3. Expand bagian **"test"** untuk melihat log real-time

**Status yang akan dilihat:**
- 🟡 **Queued** (menunggu untuk dijalankan)
- 🟡 **In progress** (sedang berjalan)
- 🟢 **Success** (semua test passed)
- 🔴 **Failed** (ada yang error)

### Step 7.3: Cara Membaca Log Pipeline

Setiap step akan menampilkan output:

```
✓ Checkout code
✓ Set up Python 3.11
✓ Install system dependencies
✓ Configure Apache for DamnCRUD
✓ Setup MySQL Database
✓ Install Python dependencies
✓ Run Pytest with Parallel Execution (xdist)
```

Di Step **"Run Pytest with Parallel Execution"**, Anda akan melihat:

**SUCCESS CASE:**
```
collected 6 items
TestDamnCRUDRead::test_tc003_view_contact_list_on_dashboard PASSED
TestDamnCRUDRead::test_tc008_access_protected_page_without_login PASSED
TestDamnCRUDCreate::test_tc004_create_new_contact PASSED
TestDamnCRUDUpdate::test_tc006_update_existing_contact PASSED
TestDamnCRUDDelete::test_tc007_delete_contact PASSED
TestCRUDIntegration::test_full_crud_workflow PASSED

===== 6 passed in 45.32s =====
```

**JIKA ADA ERROR:**
- Scroll ke bawah log untuk melihat error message
- Common errors: Database connection, Chrome driver, timeout

### Step 7.4: Download Test Report
Jika pipeline **SUCCESS** ✅:

1. Klik workflow run
2. Scroll ke bawah bagian **"Artifacts"**
3. Download file: **`test-reports`** (ZIP file yang berisi HTML report)
4. Extract dan buka file `report.html` di browser untuk melihat detail test results

---

## BAGIAN 8: Konfigurasi Lanjutan (Optional)

### Step 8.1: Tambahkan Branch Protection Rules
Untuk memastikan hanya code yang passed test bisa merge ke main:

1. Di repository, klik **"Settings"**
2. Di sidebar, klik **"Branches"**
3. Klik **"Add branch protection rule"**
4. Untuk pattern: ketik `main`
5. Centang:
   - ✅ **"Require a pull request before merging"**
   - ✅ **"Require status checks to pass before merging"**
   - ✅ **"Require branches to be up to date before merging"**
6. Under "Require status checks to pass": cari dan select **"test"**
7. Klik **"Create"**

### Step 8.2: Setup Scheduled Testing
Pipeline sudah dikonfigurasi untuk auto-run setiap hari jam 2 pagi UTC (cron job).

Untuk mengubah jadwal:

Edit file `.github/workflows/ci_cd.yml`, cari bagian:
```yaml
schedule:
  - cron: '0 2 * * *'
```

Ubah angka jam sesuai preferensi:
- `0 2 * * *` = Jam 02:00 UTC (jam 09:00 WIB)
- `0 10 * * *` = Jam 10:00 UTC (jam 17:00 WIB)
- `0 0 * * *` = Jam 00:00 UTC (jam 07:00 WIB)

### Step 8.3: Tambahkan Status Badge di README
Untuk menampilkan status CI/CD di README:

Edit `README.md` dan tambahkan:

```markdown
[![DamnCRUD CI/CD Tests](https://github.com/your-username/damncrud/workflows/DamnCRUD%20-%20Functional%20Testing%20CI%2FCD%20Pipeline/badge.svg)](https://github.com/your-username/damncrud/actions)
```

Ganti `your-username` dengan username GitHub Anda.

---

## BAGIAN 9: Troubleshooting Common Issues

### Issue 1: "Authentication failed for repository"
```
fatal: could not read Username for 'https://github.com': No error
```

**Solusi:**
- Re-setup Personal Access Token di Credential Manager (Bagian 2.4)
- Atau gunakan SSH keys (lebih advanced)

### Issue 2: "MySQL Error: Access denied for user 'root'@'localhost'"
```
mysql: [Warning] Using a password on the command line interface can be insecure.
ERROR 1045 (28000): Access denied for user 'root'@''
```

**Solusi:**
- Cek `.github/workflows/ci_cd.yml` sudah update dengan credentials benar
- Verifikasi line: `MYSQL_ROOT_PASSWORD: ''` dan `MYSQL_DATABASE: damncrud`

### Issue 3: "Chrome driver timeout - Application not responding"
```
TimeoutException: Message: timeout: Timed out receiving message from renderer
```

**Solusi:**
- Naikkan timeout di `pytest.ini` menjadi 600 (dari 300)
- Atau naikkan `--timeout-minutes` di workflow (dari 15 menjadi 20)

### Issue 4: "pytest: command not found"
```
/bin/sh: 1: pytest: command not found
```

**Solusi:**
- Cek `requirements.txt` sudah include `pytest==7.4.3`
- Cek step "Install Python dependencies" di workflow berhasil

### Issue 5: 3 Tests Failed di Parallel Execution
```
FAILED test_tc004_create_new_contact - Contact not found
FAILED test_tc006_update_existing_contact - Contact not found
FAILED test_tc007_delete_contact - Row count unchanged
```

**Solusi:**
- Ini adalah race condition yang sudah di-fix dengan locking mechanism
- Pastikan sudah update `conftest.py` dengan latest version
- Pastikan sudah update test methods dengan retry logic

---

## BAGIAN 10: Maintenance & Updates

### Menambah Test Case Baru
1. Tambah test function di `tests/test_damncrud.py`
2. Push ke GitHub:
   ```powershell
   git add tests/test_damncrud.py
   git commit -m "Add new test case TC009"
   git push
   ```
3. Pipeline otomatis akan trigger dan menjalankan semua tests

### Update Database Schema
1. Export database baru ke: `db/damncrud.sql`
2. Push ke GitHub:
   ```powershell
   git add db/damncrud.sql
   git commit -m "Update database schema"
   git push
   ```

### Update Dependencies
1. Update `requirements.txt`:
   ```powershell
   pip install --upgrade selenium pytest
   pip freeze > requirements.txt
   ```
2. Push ke GitHub:
   ```powershell
   git add requirements.txt
   git commit -m "Update dependencies"
   git push
   ```

---

## BAGIAN 11: Operasi Git Sehari-hari

### Setelah Membuat Perubahan Code
```powershell
# 1. Lihat file mana saja yang berubah
git status

# 2. Tambahkan file yang ingin di-commit
git add .

# 3. Commit dengan pesan deskriptif
git commit -m "Fix: resolusi race condition di parallel execution"

# 4. Push ke GitHub
git push
```

### Jika Ingin Membuat Branch Baru (untuk feature/fix terpisah)
```powershell
# 1. Buat branch baru
git checkout -b fix/tc007-delete-issue

# 2. Buat perubahan + commit
git add .
git commit -m "Fix TC007 delete test race condition"

# 3. Push branch baru
git push -u origin fix/tc007-delete-issue

# 4. Di GitHub, buat Pull Request (PR) dari branch ke main
# 5. Review dan merge PR
```

### Melihat History Commit
```powershell
git log --oneline -10
```

---

## ✅ Checklist: Setup Sukses

Pastikan semua ini sudah selesai:

- [ ] GitHub repository dibuat
- [ ] Personal Access Token di-generate dan disimpan di Credential Manager
- [ ] Git di-install dan di-configure dengan identity
- [ ] Repository di-initialize lokal (git init, git remote add)
- [ ] Semua file di-commit dan di-push ke GitHub
- [ ] Di repo GitHub, folder `.github/workflows/` terlihat
- [ ] GitHub Actions workflow trigger pertama kali (manual atau via commit)
- [ ] Workflow berjalan dan SUCCESS (6 passed tests)
- [ ] Test report artifact bisa di-download
- [ ] Badge status ditampilkan di README (optional)

---

## 📞 Support & Next Steps

Jika ada error atau pertanyaan:

1. **Cek log detail**: Buka workflow di GitHub → Actions → click workflow run → expand "test" step
2. **Common fixes telah dijelaskan**: Lihat Bagian 9 (Troubleshooting)
3. **Untuk advanced setup**: Hubungi untuk konfigurasi SSH keys, secrets, atau scheduled jobs yang lebih complex

---

**Happy testing! 🚀**

Sekarang setiap kali Anda push code ke GitHub, automated tests akan berjalan otomatis dan Anda bisa langsung melihat hasilnya.
