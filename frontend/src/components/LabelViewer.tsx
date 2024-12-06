import React, { useEffect, useState } from "react";
import axios from "axios";

interface LabelViewerProps {
  video: string;
}

const LabelViewer: React.FC<LabelViewerProps> = ({ video }) => {
  const [labels, setLabels] = useState<string>("");

  useEffect(() => {
    axios
      .get<string>(`http://localhost:3000/labels/${video}`)
      .then((response) => setLabels(response.data))
      .catch((error) => console.error("Error al obtener los labels:", error));
  }, [video]);

  return (
    <div>
      <h2>Labels Generados</h2>
      <pre>{labels}</pre>
    </div>
  );
};

export default LabelViewer;