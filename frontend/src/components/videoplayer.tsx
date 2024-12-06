import React from "react";
import ReactPlayer from "react-player";

interface VideoPlayerProps {
  video: string; // Nombre del video o URL proporcionada por el backend
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ video }) => {
  const videoUrl = `http://localhost:3000/videos/${video}`; // Ruta completa del video desde el backend

  return (
    <div>
      <h2>Reproduciendo: {video}</h2>
      <ReactPlayer
        url={videoUrl} // URL del video
        controls={false} // Desactiva los controles (barra de tiempo)
        width="800px" // Ancho del reproductor
        height="450px" // Alto del reproductor
        playing={true} // Reproduce automáticamente para simular streaming
        muted={false} // Cambiar a true si quieres iniciar el video en silencio
        config={{
          file: {
            attributes: {
              crossOrigin: "anonymous", // Habilita soporte CORS si es necesario
            },
          },
        }}
      />
    </div>
  );
};

export default VideoPlayer;