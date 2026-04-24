import React from "react";
import Upload from "./components/Upload";
import Search from "./components/Search";
import Chat from "./components/Chat";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>AI Document Platform</h1>

      <hr />
      <Dashboard />

      <hr />
      <Upload />

      <hr />
      <Search />

      <hr />
      <Chat />
    </div>
  );
}

export default App;