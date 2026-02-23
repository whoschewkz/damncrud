# Quick Start: Push DamnCRUD ke GitHub & Setup CI/CD

**Estimasi waktu: 10 menit total**

---

## 🚀 5 Langkah Cepat

### STEP 1: Buat Repository & Token (3 menit)

**Di GitHub.com:**
```
1. Sign in ke GitHub
2. Click "+" (top-right) → New repository
3. Nama: damncrud
4. Click "Create repository"
5. Copy URL yang dihasilkan (ex: https://github.com/your-username/damncrud.git)
6. Buat Personal Access Token:
   - Click profil → Settings → Developer settings
   - Personal access tokens → Tokens (classic) → Generate new token
   - Nama: damncrud-ci-cd, Scope: repo
   - Copy token dan simpan di tempat aman
7. Setup Credential Manager > Add credential dengan token
```

### STEP 2: Konfigurasi Git Lokal (2 menit)

**Di Windows PowerShell:**
```powershell
# 1. Install git (jika belum)
# Download dari https://git-scm.com

# 2. Setup identity
git config --global user.name "Nama Anda"
git config --global user.email "email@example.com"

# 3. Navigate ke folder project
cd C:\xampp\htdocs\DamnCRUD

# 4. Initialize git
git init
git branch -M main
git remote add origin https://github.com/your-username/damncrud.git
```

### STEP 3: Verifikasi File Penting (1 menit)

```powershell
# Di folder C:\xampp\htdocs\DamnCRUD, pastikan ada:
ls

# Harus ada:
# ✓ .github/workflows/ci_cd.yml  <- CI/CD pipeline
# ✓ tests/test_damncrud.py        <- Test automation
# ✓ tests/conftest.py             <- Test fixtures
# ✓ db/damncrud.sql               <- Database schema
# ✓ requirements.txt              <- Python dependencies
# ✓ functions.php                 <- Updated with correct DB credentials
```

### STEP 4: Commit & Push (1 menit)

```powershell
cd C:\xampp\htdocs\DamnCRUD

# Add semua file
git add .

# Commit
git commit -m "Initial commit: DamnCRUD dengan CI/CD pipeline"

# Push ke GitHub
git push -u origin main

# First time akan minta login:
# Username: your-github-username
# Password: paste PAT token (bukan password GitHub)
```

### STEP 5: Verifikasi & Run Pipeline (3 menit)

**Di GitHub:**
```
1. Refresh repository page
2. Click tab "Actions"
3. Pilih workflow "DamnCRUD - Functional Testing CI/CD Pipeline"
4. Click tombol "Run workflow"
5. Status akan berubah:
   - 🟡 Queued → In progress
   - 🟢 Success (semua 6 tests PASSED) ✓
6. Download test report dari Artifacts
```

---

## ✅ Workflow Setelah Setup

Setiap kali Anda push code:

```powershell
# 1. Buat perubahan di code
# ... edit file ...

# 2. Tambah & commit
git add .
git commit -m "Deskripsi perubahan"

# 3. Push
git push

# 4. GitHub Actions otomatis trigger
# 5. Check di tab "Actions" untuk hasil
```

---

## 📋 Troubleshooting Cepat

| Issue | Solusi |
|-------|--------|
| "Authentication failed" | Re-setup PAT di Credential Manager atau gunakan SSH keys |
| "MySQL: Access denied" | Update `.github/workflows/ci_cd.yml` sudah pakai empty password & damncrud database |
| "pytest: command not found" | Pastikan `requirements.txt` ada dan workflow install dependencies |
| "Chrome not found" | Workflow include step "Setup Chrome" - check jalankan dengan sukses |
| "3 tests failed" | Sudah fix dengan retry logic - pastikan update latest test files |

---

## 📚 Dokumentasi Lengkap

Untuk detail lengkap step-by-step, baca: **GITHUB_ACTIONS_SETUP.md**

---

**Selamat! CI/CD sudah running otomatis di GitHub! 🎉**
