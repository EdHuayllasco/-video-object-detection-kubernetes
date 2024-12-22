// bd.js
const { Pool } = require("pg");

const pool = new Pool({
    host: process.env.DB_HOST || "postgres", // Nombre del servicio de la base de datos
    port: process.env.DB_PORT || 5432,
    user: process.env.DB_USER || "admin",
    password: process.env.DB_PASSWORD || "admin",
    database: process.env.DB_NAME || "viratdata",
    ssl: {
        rejectUnauthorized: false, // Solo para pruebas
    },
});

// Confirmar la conexión
pool
    .connect()
    .then(() => console.log("Conexión exitosa con la base de datos"))
    .catch((err) => console.error("Error al conectar con la base de datos:", err));

// Exportar el objeto `pool`
module.exports = pool;