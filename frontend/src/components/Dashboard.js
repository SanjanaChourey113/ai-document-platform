import React, { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [data, setData] = useState({});

  useEffect(() => {
    axios.get("http://127.0.0.1:9000/dashboard")
      .then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Total Documents: {data.total_documents}</p>
      <p>Total Chunks: {data.total_chunks}</p>
    </div>
  );
}

export default Dashboard;