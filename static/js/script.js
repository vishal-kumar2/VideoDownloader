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
  .then(response => {
    if (!response.ok) throw new Error("Failed to download");
    return response.blob();
  })
  .then(blob => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "video.mp4";
    link.click();
    message.innerText = "✅ Video downloaded successfully!";
  })
  .catch(err => {
    message.innerText = "❌ " + err.message;
    message.style.color = "red";
  });
}
