import { useState, useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import Sidebar from "./Sidebar";
import Particles from "./Particles";

import {
  loadChats,
  saveChats,
  addMessageToChat,
  createNewChat,
  updateChatTitle,
} from "./chatManager";

import { speak, startVoiceRecognition } from "./utils/voice";

import "./App.css";

export default function App() {
  const chatEndRef = useRef(null);

  const [chats, setChats] = useState({});
  const [activeChat, setActiveChat] = useState(null);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Load chats on startup
  useEffect(() => {
    let stored = loadChats();
    if (Object.keys(stored).length === 0) {
      const id = createNewChat(stored);
      setChats(stored);
      setActiveChat(id);
    } else {
      setChats(stored);
      setActiveChat(Object.keys(stored)[0]);
    }
  }, []);

  const currentMessages =
    activeChat && chats[activeChat] ? chats[activeChat].messages : [];

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [currentMessages, loading]);

  function formatTime(date) {
    return new Date(date).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  // Handle file upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    addMessageToChat(chats, activeChat, {
      sender: "user",
      text: `📁 Uploaded File: **${file.name}**`,
      time: new Date(),
    });

    setChats({ ...chats });

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        addMessageToChat(chats, activeChat, {
          sender: "bot",
          text: `🧠 Processed File Output:\n\n${data.output}`,
          time: new Date(),
        });
        setChats({ ...chats });
      })
      .catch(() => {
        addMessageToChat(chats, activeChat, {
          sender: "bot",
          text: "⚠️ Failed to process file.",
          time: new Date(),
        });
      });
  };

  // Trigger voice input
  const handleVoiceInput = () => {
    startVoiceRecognition((transcript) => {
      setInput(transcript);
    });
  };

  async function sendMessage() {
    if (!input.trim() || !activeChat) return;

    const text = input;
    setInput("");
    setLoading(true);

    addMessageToChat(chats, activeChat, {
      sender: "user",
      text,
      time: new Date(),
    });

    setChats({ ...chats });

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          session_id: activeChat,
        }),
      });

      const data = await response.json();

      const botMessage = {
        sender: "bot",
        text: data.reply,
        time: new Date(),
      };

      addMessageToChat(chats, activeChat, botMessage);

      // Auto title based on reply
      updateChatTitle(
        chats,
        activeChat,
        data.reply.slice(0, 45).replace(/\n/g, " ")
      );

      saveChats(chats);
      setChats({ ...chats });
    } catch {
      addMessageToChat(chats, activeChat, {
        sender: "bot",
        text: "⚠️ Server error.",
        time: new Date(),
      });
      setChats({ ...chats });
    }

    setLoading(false);
  }

  return (
    <div className="app-layout">

      {/* Subtle Particle Background */}
      <Particles />

      {/* Sidebar */}
      <Sidebar
        chats={chats}
        setChats={setChats}
        activeChat={activeChat}
        setActiveChat={setActiveChat}
        onFileUpload={handleFileUpload}
        onVoiceInput={handleVoiceInput}
      />

      {/* Main Chat */}
      <div className="chat-container">
        <div className="chat-box neon-panel">
          {currentMessages.map((m, index) => (
            <div key={index} className={`message-row ${m.sender}`}>
              {m.sender === "bot" && (
                <img src="/bot.png" alt="Bot" className="avatar" />
              )}

              <div className={`message ${m.sender}-msg neon-msg`}>
                <ReactMarkdown>{m.text}</ReactMarkdown>

                <div className="controls">
                  <span className="timestamp">{formatTime(m.time)}</span>

                  {m.sender === "bot" && (
                    <button
                      className="speak-btn"
                      onClick={() => speak(m.text)}
                    >
                      🔊
                    </button>
                  )}
                </div>
              </div>

              {m.sender === "user" && (
                <img src="/user.png" alt="User" className="avatar" />
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <img src="/bot.png" className="avatar" alt="Bot" />
              <div className="bot-msg typing">Assistant is typing…</div>
            </div>
          )}

          <div ref={chatEndRef}></div>
        </div>

        {/* Input Area */}
        <div className="input-area">
          <button className="voice-btn" onClick={handleVoiceInput}>
            🎤
          </button>

          <input
            type="text"
            value={input}
            placeholder="Type a message..."
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          <button className="send-btn neon-button" onClick={sendMessage}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}
