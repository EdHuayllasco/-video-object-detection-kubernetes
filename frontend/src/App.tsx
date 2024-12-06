import React from "react";
import { BrowserRouter as Router, Routes, Route, useParams } from "react-router-dom";
import VideoList from "./components/VideoList";
import VideoPlayer from "./components/videoplayer";
import LabelViewer from "./components/LabelViewer";

const VideoDetail: React.FC = () => {
  const { video } = useParams<{ video: string }>();

  if (!video) return <div>No se seleccionó un video.</div>;

  return (
    <div>
      <VideoPlayer video={video} />
      <LabelViewer video={video} />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<VideoList />} />
        <Route path="/video/:video" element={<VideoDetail />} />
      </Routes>
    </Router>
  );
};

export default App;