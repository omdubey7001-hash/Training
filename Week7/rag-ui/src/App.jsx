import { useState } from "react";

export default function App() {

  const [input, setInput] = useState("");
  const [mode, setMode] = useState("ask");
  const [messages, setMessages] = useState([]);
  const [file, setFile] = useState(null);

  async function sendMessage() {

    if (!input.trim() && !file) return;

    const userMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);

    let endpoint = "ask";
    let options = {};

    // ---------------- TEXT MODE ----------------
    if (mode === "ask") {
      endpoint = "ask";
      options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input })
      };
    }

    // ---------------- SQL MODE ----------------
    if (mode === "sql") {
      endpoint = "ask-sql";
      options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input })
      };
    }

    // ---------------- IMAGE MODE (UPLOAD) ----------------
    if (mode === "image") {
      endpoint = "ask-image";

      const formData = new FormData();
      formData.append("file", file);

      options = {
        method: "POST",
        body: formData
      };
    }

    const res = await fetch(`http://127.0.0.1:8000/${endpoint}`, options);
    const data = await res.json();

    const botMsg = {
      role: "bot",
      text: data.answer,
      confidence: data.confidence,
      hallucination: data.hallucination,
      image: data.image   
    };

    setMessages(prev => [...prev, botMsg]);

    setInput("");
    setFile(null);
  }

  return (
    <div style={{background:"#020617",height:"100vh",color:"white",padding:"20px"}}>

      <h2>Enterprise RAG Assistant</h2>

      {/* MODE BUTTONS */}
      <div style={{marginBottom:"10px"}}>
        <button onClick={()=>setMode("ask")}>Ask</button>
        <button onClick={()=>setMode("image")} style={{marginLeft:"10px"}}>Ask Image</button>
        <button onClick={()=>setMode("sql")} style={{marginLeft:"10px"}}>Ask SQL</button>
      </div>

      {/* CHAT WINDOW */}
      <div style={{height:"65vh",overflowY:"auto"}}>

        {messages.map((m,i)=>(
          <div key={i} style={{
            background:m.role==="user" ? "#1e293b" : "#0f172a",
            padding:"12px",
            margin:"10px 0",
            borderRadius:"8px"
          }}>
            <b>{m.role==="user" ? "You" : "RAG"}:</b>

            <div>{m.text}</div>

            {/* IMAGE SHOW FIX */}
            {m.image && (
              <img
                src={m.image}
                alt="rag"
                style={{
                  width:"300px",
                  marginTop:"10px",
                  borderRadius:"8px",
                  border:"1px solid #334155"
                }}
              />
            )}

            {m.role==="bot" && (
              <div style={{fontSize:"12px",opacity:0.7}}>
                Confidence: {m.confidence} | Hallucination: {String(m.hallucination)}
              </div>
            )}
          </div>
        ))}

      </div>

      {/* INPUT AREA */}
      {mode !== "image" && (
        <input
          value={input}
          onChange={e=>setInput(e.target.value)}
          placeholder="Ask something..."
          style={{width:"70%",padding:"10px"}}
        />
      )}

      {/* IMAGE UPLOAD INPUT */}
      {mode === "image" && (
        <input
          type="file"
          onChange={(e)=>setFile(e.target.files[0])}
        />
      )}

      <button
        onClick={sendMessage}
        style={{padding:"10px",marginLeft:"10px"}}
      >
        Send
      </button>

    </div>
  );
}
