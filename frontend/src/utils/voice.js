export function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1;
  utter.pitch = 1;
  utter.voice = speechSynthesis.getVoices()[0];
  speechSynthesis.speak(utter);
}

export function startVoiceRecognition(callback) {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Voice recognition not supported in this browser.");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    callback(transcript);
  };
}
