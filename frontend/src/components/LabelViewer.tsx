import React, { useEffect, useState } from "react";
import axios from "axios";

interface LabelViewerProps {
  video: string; // Nombre base del video
}

interface ClassData {
  class: number; // Número de la clase
}

const classMapping: { [key: number]: string } = {
  0: "Car",
  1: "Motorbike",
  2: "Person",
};

const LabelViewer: React.FC<LabelViewerProps> = ({ video }) => {
  const [classes, setClasses] = useState<ClassData[]>([]);

  useEffect(() => {
    // Llama al endpoint y extrae la propiedad 'classes' de la respuesta
    axios
      .get<{ videoId: number; classes: ClassData[] }>(
        `http://a9cc9376789394999978f948dffe9b8f-387308753.us-east-1.elb.amazonaws.com/labels/${video}`
      )
      .then((response) => {
        setClasses(response.data.classes); // Guarda solo la propiedad 'classes'
      })
      .catch((error) => console.error("Error al obtener las clases:", error));
  }, [video]);

  return (
    <div>
      <h2>Clases Generadas</h2>
      {classes.length === 0 ? (
        <p>No se encontraron clases para este video.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {classes.map((item, index) => (
            <li key={index} style={{ marginBottom: "0.5rem" }}>
              <button
                onClick={() =>
                  alert(`Has hecho clic en: ${classMapping[item.class]}`)
                }
                style={{
                  padding: "0.5rem 1rem",
                  backgroundColor: "#4CAF50",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                  fontSize: "1rem",
                }}
              >
                {classMapping[item.class] || "Clase Desconocida"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default LabelViewer;