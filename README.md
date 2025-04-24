# 🧩 Dokumentasi Komunikasi Antar Layanan

## 📖 Deskripsi Umum
Sistem yang kami buat terdiri dari 3 layanan yang berkomunikasi menggunakan protokol HTTP dan format data JSON, tanpa perantara API Gateway. Setiap layanan memiliki peran **provider** dan/atau **consumer**, sesuai dengan  ketentuan dari service-to-service communication.

---

## 🗂 Layanan yang Digunakan

| Service Name         | Port   | Deskripsi                                 |
|----------------------|--------|-------------------------------------------|
| `student_service`    | 8001   | Menyediakan data mahasiswa                |
| `internship_service` | 8002   | Menyediakan data program magang           |
| `application_service`| 8003   | Memproses dan menyimpan aplikasi magang   |

---

## 🔄 Alur Komunikasi Antar Layanan

### 1. Endpoint: `POST /apply` (application_service)
- **Consumer**: `application_service`
- **Provider**: `student_service`, `internship_service`

#### 📋 Deskripsi Proses:
1. Menerima data aplikasi dari client berupa `student_id` dan `internship_id`.
2. Mengecek keberadaan mahasiswa dengan request ke:
   ```
   GET http://localhost:8001/students/{student_id}
   ```
3. Mengecek keberadaan program magang dengan request ke:
   ```
   GET http://localhost:8002/internships/{internship_id}
   ```
4. Jika keduanya valid, data aplikasi disimpan dengan status default: `pending`.

---

### 2. Endpoint: `GET /applications` (application_service)
- **Consumer**: `application_service`
- **Provider**: `student_service`, `internship_service`

#### 📋 Deskripsi Proses:
1. Mengambil seluruh data aplikasi.
2. Untuk setiap aplikasi, mengambil data mahasiswa dari:
   ```
   GET http://localhost:8001/students/{id}
   ```
3. Mengambil data program magang dari:
   ```
   GET http://localhost:8002/internships/{id}
   ```
4. Mengembalikan response lengkap dengan informasi `student` dan `internship`.

---

## 📦 Format Pertukaran Data (JSON)

### 🔹 Student Service
```json
{
  "id": 1,
  "name": "Rina",
  "major": "Informatika"
}
```

### 🔹 Internship Service
```json
{
  "id": 2,
  "title": "Data Analyst Intern",
  "company": "DataLabs"
}
```

### 🔹 Application Service (Response POST /apply)
```json
{
  "id": 1,
  "student_id": 1,
  "internship_id": 2,
  "status": "pending"
}
```

---

## 🔁 Ringkasan Peran Tiap Service

| Service              | Sebagai Provider              | Sebagai Consumer              |
|----------------------|-------------------------------|-------------------------------|
| `student_service`     | Data Mahasiswa (`/students`)   | —                             |
| `internship_service`  | Data Magang (`/internships`)   | —                             |
| `application_service` | Data Aplikasi (`/applications`) | Mahasiswa & Magang            |

---

## ⚙️ Teknologi yang Digunakan
- **Framework**: FastAPI (Python)
- **Protokol**: HTTP
- **Format Data**: JSON
- **Komunikasi**: Langsung antar service (service-to-service)
- **Host**: Localhost dengan port berbeda

---

## 📌 Catatan
- Endpoint pada masing-masing layanan didokumentasikan otomatis oleh FastAPI melalui Swagger UI di `/docs`.
- Dokumentasi ini difokuskan pada komunikasi antar service, bukan interaksi dengan frontend/client.