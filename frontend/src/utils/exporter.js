export function exportTxt(messages) {
  const text = messages
    .map((m) => `${m.sender.toUpperCase()}: ${m.text}\n`)
    .join("\n");

  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "chat_export.txt";
  a.click();
}

export function exportJson(messages) {
  const blob = new Blob([JSON.stringify(messages, null, 2)], {
    type: "application/json",
  });

  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "chat_export.json";
  a.click();
}
