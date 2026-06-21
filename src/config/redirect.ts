/**
 * Konfigurasi Redirect
 * Link tujuan setelah verifikasi selesai
 * Bisa diganti sesuai kebutuhan
 */

export const REDIRECT_CONFIG = {
  // Link tujuan redirect
  targetUrl: "https://youtu.be/dQw4w9WgXcQ", // Contoh: Rick Roll
  
  // Durasi countdown sebelum redirect (detik)
  countdownDuration: 5,
  
  // Pesan yang ditampilkan selama countdown
  messages: {
    title: "Verifikasi Selesai",
    description: "Anda akan dialihkan ke halaman tujuan dalam:",
    countdownText: "detik",
    redirectingText: "Mengarahkan ke halaman yang diminta...",
    buttonText: "Lanjutkan Sekarang",
    
    // Pesan sukses
    successTitle: "✓ Verifikasi Berhasil",
    successMessage: "Semua data telah diverifikasi dengan aman."
  },
  
  // Warna untuk UI
  colors: {
    primary: "#2563eb", // blue-600
    success: "#16a34a", // green-600
    warning: "#dc2626", // red-600 (untuk countdown akhir)
    background: "rgba(0, 0, 0, 0.8)"
  }
} as const;

/**
 * Fungsi untuk mendapatkan konfigurasi redirect
 * Bisa di-extend untuk mengambil dari environment variables
 */
export function getRedirectConfig() {
  // Di production, bisa ambil dari environment variables
  const envUrl = process.env.NEXT_PUBLIC_REDIRECT_URL;
  
  return {
    ...REDIRECT_CONFIG,
    targetUrl: envUrl || REDIRECT_CONFIG.targetUrl
  };
}