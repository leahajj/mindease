// Navigate between pages
function goTo(page) {
    window.location.href = page;
  }
  
  // Send message function for Chat Screen
  function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
  
    if (!input || !chatBox) return; // Prevent errors if elements don't exist
  
    const userMessage = input.value.trim();
    if (!userMessage) return; // Ignore empty messages
  
    // Create user message bubble
    const userDiv = document.createElement("div");
    userDiv.classList.add("user-bubble");
    userDiv.textContent = userMessage;
    chatBox.appendChild(userDiv);
  
    // Create chatbot reply
    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-bubble");
    botDiv.textContent = getBotReply(userMessage);
    chatBox.appendChild(botDiv);
  
    // Clear input and scroll down
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  
  // Simple chatbot responses
  function getBotReply(message) {
    const lower = message.toLowerCase();
  
    if (lower.includes("hi") || lower.includes("hello")) {
      return "Hi there! How are you feeling today? 💬";
    } else if (lower.includes("sad") || lower.includes("tired")) {
      return "I'm sorry to hear that. Remember, it’s okay to rest 💙";
    } else if (lower.includes("happy") || lower.includes("good")) {
      return "That’s wonderful! Keep it up 🌈";
    } else if (lower.includes("stress")) {
      return "Try taking a deep breath. You’ve got this 🌤";
    } else {
      return "I'm here for you — tell me more!";
    }
  }
  