import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const VideoList: React.FC = () => {
  const [videos, setVideos] = useState<string[]>([]);

  useEffect(() => {
    axios
      .get<string[]>("http://localhost:3000/videos")
      .then((response) => setVideos(response.data))
      .catch((error) => console.error("Error al obtener los videos:", error));
  }, []);

  return (
    <div>
      <h2>Videos Procesados</h2>
      <ul>
        {videos.map((video, index) => (
          <li key={index}>
            <Link to={`/video/${video}`}>{video}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoList;