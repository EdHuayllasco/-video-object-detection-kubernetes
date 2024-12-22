import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

// Interfaz para los videos
interface Video {
  id: number;
  name: string;
  created_at: string;
}

const VideoList: React.FC = () => {
  const [videos, setVideos] = useState<Video[]>([]); // Estado para almacenar los videos
  const [error, setError] = useState<string | null>(null); // Estado para almacenar errores
  const [loading, setLoading] = useState<boolean>(true); // Estado para manejar el indicador de carga

  // Efecto para obtener los datos del backend
  useEffect(() => {
    axios
      .get<Video[]>("http://a9cc9376789394999978f948dffe9b8f-387308753.us-east-1.elb.amazonaws.com/videos") // URL del backend
      .then((response) => {
        setVideos(response.data); // Establece los datos obtenidos
        setError(null); // Limpia errores previos si los hay
      })
      .catch((error) => {
        console.error("Error al obtener los videos:", error);
        setError("No se pudieron cargar los videos.");
      })
      .finally(() => setLoading(false)); // Finaliza el estado de carga
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>Videos Procesados</h2>

      {/* Mostrar indicador de carga */}
      {loading && <p>Cargando videos...</p>}

      {/* Mostrar mensaje de error si ocurre */}
      {error && !loading && <p style={{ color: "red" }}>{error}</p>}

      {/* Mostrar lista de videos si están disponibles */}
      {!loading && !error && videos.length > 0 ? (
        <ul>
          {videos.map((video) => (
            <li key={video.id}>
              <Link to={`/video/${video.name}`} style={{ textDecoration: "none", color: "#007bff" }}>
                {video.name}
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        // Mensaje si no hay videos disponibles
        !loading &&
        !error && <p style={{ color: "gray" }}>No hay videos disponibles.</p>
      )}
    </div>
  );
};

export default VideoList;