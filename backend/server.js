const express = require("express");
const cors = require("cors");
const fs = require("fs");
const path = require("path");
const pool = require('./bd.js');

const app = express();
const PORT = 3000;

// Permitir solicitudes CORS
app.use(cors());
const baseURL = "https://viratvideos.s3.us-east-1.amazonaws.com"; // Base URL de tus videos en S3
// Endpoint para obtener todos los videos
app.get('/videos', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM videos'); // Consulta a la base de datos
        res.json(result.rows); // Devuelve los datos en formato JSON
    } catch (err) {
        console.error('Error ejecutando la consulta:', err);
        res.status(500).json({ error: 'Error al obtener los videos' }); // Devuelve un error en caso de fallo
    }
});

// Ruta para servir un video procesado
app.get("/videos/:video", (req, res) => {
    let { video } = req.params;

    // Reemplazar la extensión .mp4 por .avi
    const videoBaseName = path.parse(video).name;
    const newVideoName = `${videoBaseName}.avi`;

    // Construir la URL del archivo en S3
    const videoUrl = `https://viratvideos.s3.us-east-1.amazonaws.com/${videoBaseName}/${newVideoName}`;

    console.log("Redirigiendo al archivo en S3:", videoUrl);

    // Redirigir al archivo en S3
    res.redirect(videoUrl);
});
// Ruta para obtener labels y clases únicas asociadas desde la base de datos
app.get("/labels/:video", async (req, res) => {
    const { video } = req.params;

    // Obtener el nombre base del video (sin extensión)const videoBaseName = path.parse(video).name;

    try {
        // Paso 1: Buscar el video en la tabla 'videos' y obtener su ID
        const videoQuery = 'SELECT id FROM videos WHERE name = $1';
        const videoResult = await pool.query(videoQuery, [video]);

        if (videoResult.rows.length === 0) {
            return res.status(404).json({ error: "Video no encontrado en la base de datos." });
        }

        const videoId = videoResult.rows[0].id;

        // Paso 2: Obtener clases únicas asociadas al video desde 'class_intervals'
        const classesQuery = `
        SELECT DISTINCT ON (class) class, start_frame, end_frame
        FROM class_intervals
        WHERE video_id = $1
        ORDER BY class, start_frame ASC
        `;
        const classesResult = await pool.query(classesQuery, [videoId]);

        if (classesResult.rows.length === 0) {
            return res.status(404).json({ error: "No se encontraron clases para este video." });
        }

        // Mapear resultados para enviar clases únicas
        const uniqueClasses = classesResult.rows.map(row => ({
            class: row.class,
            start_frame: row.start_frame,
            end_frame: row.end_frame
        }));

        // Enviar la respuesta con las clases únicas
        res.json({
            videoId: videoId,
            classes: uniqueClasses
        });
    } catch (error) {
        console.error("Error al obtener las clases desde la base de datos:", error);
        res.status(500).json({ error: "Error al procesar los datos." });
    }
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Backend escuchando en http://localhost:${PORT}`);
});