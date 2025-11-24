// Handles multi-chat sessions with localStorage

const STORAGE_KEY = "multi_chat_sessions";

export function loadChats() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : {};
}

export function saveChats(chats) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
}

export function createNewChat(chats) {
  const id = crypto.randomUUID();
  chats[id] = {
    id,
    title: "New Chat",
    messages: [
      {
        sender: "bot",
        text: "Hello! I’m your Company Research Assistant. How can I help you today?",
        time: new Date(),
      }
    ],
  };
  saveChats(chats);
  return id;
}

export function updateChatTitle(chats, chatId, newTitle) {
  if (chats[chatId]) {
    chats[chatId].title = newTitle;
    saveChats(chats);
  }
}

export function addMessageToChat(chats, chatId, message) {
  if (!chats[chatId]) return;
  chats[chatId].messages.push(message);
  saveChats(chats);
}
