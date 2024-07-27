import React from "react";
import FileUpload from "./FileUpload";
import "./App.css"

export const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Document Summarizer</h1>
        <FileUpload />
      </header>
    </div>
  );
};

export default App;
