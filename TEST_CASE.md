# DamnCRUD - Functional Testing Documentation

## Test Case Summary

Aplikasi DamnCRUD adalah aplikasi CRUD (Create, Read, Update, Delete) untuk manajemen kontak. Dokumentasi ini berisi test case untuk functional testing aplikasi.

**Kredensial Login:**
- Username: `admin`
- Password: `nimda666!`

---

## Detailed Test Cases

### TC001: Successful Login
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC001 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat login dengan kredensial yang valid |
| **TEST CASE DESCRIPTION** | 1. Buka halaman login<br>2. Masukkan username: admin<br>3. Masukkan password: nimda666!<br>4. Klik tombol "OK I'm sign in" |
| **EXPECTED RESULT** | Pengguna berhasil login dan dialihkan ke halaman dashboard (index.php) |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC002: Failed Login with Invalid Credentials
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC002 |
| **TEST CASE OBJECTIVE** | Memverifikasi sistem menolak login dengan kredensial yang tidak valid |
| **TEST CASE DESCRIPTION** | 1. Buka halaman login<br>2. Masukkan username: admin<br>3. Masukkan password: wrongpassword<br>4. Klik tombol "OK I'm sign in" |
| **EXPECTED RESULT** | Halaman login tetap ditampilkan dengan pesan error "Damn, wrong credentials!!" |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC003: View Contact List on Dashboard
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC003 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat melihat daftar kontak di dashboard |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Sistem menampilkan halaman dashboard<br>3. Verifikasi tabel kontak ditampilkan dengan kolom: #, Name, Email, Phone, Title, Created |
| **EXPECTED RESULT** | Halaman dashboard menampilkan tabel kontak dengan semua kolom yang sesuai |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC004: Create New Contact
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC004 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat menambahkan kontak baru |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol "Add New Contact"<br>3. Isi form dengan data:<br>   - Name: John Doe<br>   - Email: john.doe@email.com<br>   - Phone: 08123456789<br>   - Title: Software Engineer<br>4. Klik tombol "Save" |
| **EXPECTED RESULT** | Kontak baru berhasil ditambahkan dan halaman dialihkan ke dashboard. Kontak baru muncul di tabel kontak |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC005: Create Contact with Empty Required Fields
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC005 |
| **TEST CASE OBJECTIVE** | Memverifikasi validasi form ketika required fields kosong |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol "Add New Contact"<br>3. Kosongkan field Name dan Email<br>4. Isi field Phone dan Title<br>5. Klik tombol "Save" |
| **EXPECTED RESULT** | Form tidak dapat disubmit, browser menampilkan validasi HTML5 untuk required fields |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC006: Update Existing Contact
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC006 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat mengubah data kontak yang ada |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol edit/update pada salah satu kontak<br>3. Ubah data:<br>   - Name: Jane Smith (sebelumnya: John Doe)<br>   - Email: jane.smith@email.com<br>4. Klik tombol "Update" |
| **EXPECTED RESULT** | Data kontak berhasil diubah dan halaman dialihkan ke dashboard. Data terbaru ditampilkan di tabel |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC007: Delete Contact
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC007 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat menghapus kontak |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol delete pada salah satu kontak<br>3. Konfirmasi penghapusan jika ada dialog |
| **EXPECTED RESULT** | Kontak berhasil dihapus dan tidak lagi muncul di tabel kontak. Halaman dialihkan ke dashboard |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC008: Access Protected Page Without Login
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC008 |
| **TEST CASE OBJECTIVE** | Memverifikasi halaman yang dilindungi tidak dapat diakses tanpa login |
| **TEST CASE DESCRIPTION** | 1. Buka browser<br>2. Akses langsung ke URL: http://localhost/DamnCRUD/index.php<br>3. Tidak melakukan login |
| **EXPECTED RESULT** | Pengguna diarahkan kembali ke halaman login |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC009: Successfully Logout
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC009 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat logout dengan sukses |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol "Sign out" |
| **EXPECTED RESULT** | Session berakhir dan pengguna diarahkan ke halaman login. Browser tidak dapat kembali ke halaman dashboard |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

### TC010: View User Profile Page
| Attribute | Nilai |
|-----------|-------|
| **TEST CASE ID** | TC010 |
| **TEST CASE OBJECTIVE** | Memverifikasi pengguna dapat membuka halaman profil |
| **TEST CASE DESCRIPTION** | 1. Login dengan kredensial yang valid<br>2. Klik tombol "Profil" di menu navigasi |
| **EXPECTED RESULT** | Halaman profil berhasil ditampilkan |
| **ACTUAL RESULT** | - |
| **PASS/FAIL** | - |

---

## Test Cases yang Akan Diotomasi (5 Test Cases)

Untuk soal nomor 3 (otomasi dengan Python + Selenium), berikut adalah 5 test case yang akan diotomasi:

1. **TC004** - Create New Contact ✅
2. **TC003** - View Contact List on Dashboard ✅
3. **TC006** - Update Existing Contact ✅
4. **TC007** - Delete Contact ✅
5. **TC008** - Access Protected Page Without Login ✅

*(Mengecualikan TC001/TC002 yang merupakan login dan logout)*

---

## Environment Setup

- **Browser:** Chrome/Chromium
- **Server:** XAMPP (Apache + MySQL)
- **Database:** badcrud
- **Base URL:** http://localhost/DamnCRUD/
- **Testing Framework:** Pytest + Selenium WebDriver
- **CI/CD:** Github Actions

---

## Test Execution Notes

- Setiap test case dijalankan secara independen
- Database direset sebelum dan sesudah test untuk consistency
- Implicit wait: 10 detik
- Screenshot diambil untuk failed test cases
