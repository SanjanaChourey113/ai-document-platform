import React, { useState } from "react";
import axios from "axios";

function Search() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState("");

  const handleSearch = async () => {
    const res = await axios.get(`http://127.0.0.1:9000/search?query=${query}`);
    setResult(JSON.stringify(res.data, null, 2));
  };

  return (
    <div>
      <h2>Search</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleSearch}>Search</button>

      <pre>{result}</pre>
    </div>
  );
}

export default Search;