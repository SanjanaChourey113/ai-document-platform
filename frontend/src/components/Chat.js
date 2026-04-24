import React, { useState } from "react";
import axios from "axios";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {
    const res = await axios.post("http://127.0.0.1:9000/ask", {
      question: question
    });

    setAnswer(JSON.stringify(res.data, null, 2));
  };

  return (
    <div>
      <h2>Ask Questions</h2>
      <input value={question} onChange={(e) => setQuestion(e.target.value)} />
      <button onClick={askQuestion}>Ask</button>

      <pre>{answer}</pre>
    </div>
  );
}

export default Chat;