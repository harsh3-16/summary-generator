import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const uploadResponse = await axios.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const filename = uploadResponse.data.filename;
      const summarizeResponse = await axios.post("/summarize", { filename });

      setSummary(summarizeResponse.data.summary);
    } catch (err) {
      console.error(err);
    }
  };


  return (
    <div>
        <input className="input" type="file" onChange={handleFileChange} />
        <button onClick = {handleUpload}>Upload and Summarize</button>

        <div className="summary">
            <h3>Summary:</h3>
            <p>{summary}</p>
        </div>
    </div>
  );
};

export default FileUpload;
