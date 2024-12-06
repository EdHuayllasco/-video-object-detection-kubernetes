const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

// Permitir solicitudes CORS
app.use(cors());

// Ruta para obtener la lista de videos procesados
app.get("/videos", (req, res) => {
  const videoDir = path.join(__dirname, "../viratvideos/results/predict");
  fs.readdir(videoDir, (err, files) => {
    if (err) {
      return res.status(500).json({ error: "Error al leer los videos procesados" });
    }
    const videos = files.filter((file) => file.endsWith(".mp4") || file.endsWith(".avi"));
    res.json(videos);
  });
});

// Ruta para servir un video procesado
app.get("/videos/:video", (req, res) => {
  const { video } = req.params;
  const videoPath = path.join(__dirname, "../viratvideos/results/predict", video);
  res.sendFile(videoPath);
});

// Ruta para obtener los labels de un video
app.get("/labels/:video", (req, res) => {
  const { video } = req.params;
  const videoName = path.parse(video).name; // Sin extensión
  const labelPath = path.join(__dirname, "../viratvideos/results/predict/labels", `${videoName}.txt`);
  if (!fs.existsSync(labelPath)) {
    return res.status(404).json({ error: "Labels no encontrados" });
  }
  const labels = fs.readFileSync(labelPath, "utf-8");
  res.send(labels);
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Backend escuchando en http://localhost:${PORT}`);
});