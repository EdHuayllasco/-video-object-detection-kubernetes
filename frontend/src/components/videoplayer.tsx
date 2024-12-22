import React from "react";
import ReactPlayer from "react-player";

interface VideoPlayerProps {
  video: string; // Nombre del video o URL proporcionada por el backend
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ video }) => {
  const sanitizedVideoName = video.replace(/\.mp4$/, ".avi"); 
  const videoUrl = `http://a9cc9376789394999978f948dffe9b8f-387308753.us-east-1.elb.amazonaws.com/videos/${sanitizedVideoName}`; // Ruta completa del video desde el backend
  console.log(videoUrl);

  return (
    <div>
      <h2>Reproduciendo: {sanitizedVideoName}</h2>
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