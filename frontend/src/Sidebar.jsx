import { exportTxt, exportJson } from "./utils/exporter";

export default function Sidebar({
  chats,
  activeChat,
  setActiveChat,
  setChats,
  onFileUpload,
  onVoiceInput,
}) {
  function clearChat() {
    setChats({
      ...chats,
      [activeChat]: {
        ...chats[activeChat],
        messages: [
          {
            sender: "bot",
            text: "Chat cleared! How can I help you next?",
            time: new Date(),
          },
        ],
      },
    });
  }

  return (
    <div className="sidebar neon-soft">
      <h2 className="sidebar-title">Workspace</h2>

      <button className="sidebar-btn" onClick={() => onVoiceInput()}>
        🎤 Voice Input
      </button>

      <label className="sidebar-btn">
        📁 Upload File
        <input type="file" hidden onChange={onFileUpload} />
      </label>

      <button className="sidebar-btn" onClick={() => exportTxt(chats[activeChat].messages)}>
        📝 Export TXT
      </button>

      <button className="sidebar-btn" onClick={() => exportJson(chats[activeChat].messages)}>
        🧠 Export JSON
      </button>

      <button className="sidebar-btn danger" onClick={clearChat}>
        🧹 Clear Chat
      </button>

      <h3 className="sidebar-subtitle">Chats</h3>

      <div className="chat-history">
        {Object.values(chats).map((chat) => (
          <div
            key={chat.id}
            className={`chat-history-item ${
              chat.id === activeChat ? "active" : ""
            }`}
            onClick={() => setActiveChat(chat.id)}
          >
            {chat.title}
          </div>
        ))}
      </div>
    </div>
  );
}
