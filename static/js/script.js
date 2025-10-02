function downloadVideo() {
  const url = document.getElementById("videoURL").value;
  const quality = document.getElementById("quality").value;
  const message = document.getElementById("message");

  if (!url) {
    message.innerText = "⚠️ Please enter a video URL.";
    message.style.color = "red";
    return;
  }

  message.style.color = "green";
  message.innerText = "✅ Downloading...";

  fetch("/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, quality })
  })
  .then(async response => {
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.error || "Failed to download");
    }
    return response.blob();
  })
  .then(blob => {
    // Create a unique filename using timestamp
    const filename = `video_${Date.now()}.mp4`;
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    message.innerText = "✅ Video downloaded successfully!";
  })
  .catch(err => {
    message.innerText = "❌ " + err.message;
    message.style.color = "red";
  });
}
