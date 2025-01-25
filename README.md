# Simple Spoon - Aplikasi Resep Makanan

Aplikasi web resep makanan berbasis Django yang memungkinkan pengguna untuk mencari dan berbagi resep makanan.

## Prasyarat

Sebelum menjalankan aplikasi ini, pastikan Anda telah menginstal:

- Docker
- Docker Compose

## Cara Menjalankan Aplikasi

1. Clone repositori ini:
   ```bash
   git clone <repository-url>
   cd django-resep/app
   ```

2. Buat file `.env` dari contoh yang tersedia:
   ```bash
   cp .env.example .env
   ```

3. Isi file `.env` dengan konfigurasi yang sesuai:
   ```
   ENVIRONMENT = prod
   EMAIL_HOST_USER = your-email@example.com
   EMAIL_HOST_PASSWORD = your-email-password
   CLOUDINARY_CLOUD_NAME = your-cloudinary-name
   CLOUDINARY_API_KEY = your-cloudinary-key
   CLOUDINARY_API_SECRET = your-cloudinary-secret
   GOOGLE_API_KEY = your-google-api-key
   DB_URL = postgres://root:root@db:5432/resep
   POSTGRES_DB = resep
   POSTGRES_USER = root
   POSTGRES_PASSWORD = root
   SECRET_KEY = your-django-secret-key
   ```

4. Jalankan aplikasi menggunakan Docker Compose:
   ```bash
   docker compose up -d
   ```

5. Aplikasi sekarang dapat diakses melalui:
   - http://localhost (untuk akses lokal)
   - https://simplespoon.online (untuk akses produksi)

## Fitur Aplikasi

- Pencarian resep makanan
- Berbagi resep makanan
- Integrasi dengan YouTube untuk video tutorial
- Upload gambar resep menggunakan Cloudinary
- Sistem autentikasi pengguna

## Struktur Proyek

```
app/
├── main/           # Aplikasi utama Django
├── resep/          # Konfigurasi proyek Django
├── staticfiles/    # File statis (CSS, JS, Images)
├── compose.yaml    # Konfigurasi Docker Compose
├── Caddyfile      # Konfigurasi server Caddy
└── .env           # File konfigurasi environment
```

## Layanan yang Digunakan

Aplikasi ini menggunakan beberapa layanan:
- Django (Backend)
- PostgreSQL (Database)
- Caddy (Web Server)
- Cloudinary (Penyimpanan Media)
- YouTube API (Integrasi Video)

## Troubleshooting

Jika mengalami masalah:

1. Periksa log container:
   ```bash
   docker compose logs
   ```

2. Restart layanan:
   ```bash
   docker compose restart
   ```

3. Rebuild dan jalankan ulang:
   ```bash
   docker compose down
   docker compose up -d --build
   ```

## Menghentikan Aplikasi

Untuk menghentikan aplikasi:
```bash
docker compose down
```
