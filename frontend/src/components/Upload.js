import React, { useState } from "react";
import axios from "axios";

function Upload() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://127.0.0.1:9000/upload", formData);
    setResponse(JSON.stringify(res.data, null, 2));
  };

  return (
    <div>
      <h2>Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>

      <pre>{response}</pre>
    </div>
  );
}

export default Upload;