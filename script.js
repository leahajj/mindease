
// NAVIGATION

function goTo(page) {
  window.location.href = page;
}



//  FUNCTIONS

function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");

  if (!input || !chatBox) return;

  const userMessage = input.value.trim();
  if (!userMessage) return;

  const userDiv = document.createElement("div");
  userDiv.classList.add("user-bubble");
  userDiv.textContent = userMessage;
  chatBox.appendChild(userDiv);

  // BOT REPLY (fallback)
  const botDiv = document.createElement("div");
  botDiv.classList.add("bot-bubble");
  botDiv.textContent = getBotReply(userMessage);
  chatBox.appendChild(botDiv);

  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotReply(message) {
  const lower = message.toLowerCase();
  if (lower.includes("recommend") || lower.includes("help")) {
      // Trigger recommendation microservice
      getRecommendations(2); // default mood_score = 2 (sad)
      return "Let me get some personalized recommendations for you…";
  }
  if (lower.includes("hi") || lower.includes("hello")) return "Hi there! How are you feeling today? 💬";
  if (lower.includes("sad") || lower.includes("tired")) return "I'm sorry to hear that. Remember, it's okay to rest 💙";
  if (lower.includes("happy")) return "That's wonderful! Keep it up 🌈";
  return "I'm here for you — tell me more!";
}

function openEndChatPopup() { document.getElementById("endChatPopup").style.display = "flex"; }
function closeEndChatPopup() { document.getElementById("endChatPopup").style.display = "none"; }
function openSaveChatPopup() { document.getElementById("saveChatPopup").style.display = "flex"; }
function closeSaveChatPopup() { document.getElementById("saveChatPopup").style.display = "none"; }


// -----------------------------
// MOOD LOGGER (POST) — MoodLogger.py (port 8000)
// -----------------------------
function logMood() {
  const mood = document.getElementById("moodInput").value;
  const date = new Date().toISOString().split("T")[0];
  const journal = document.getElementById("journalInput").value;

  fetch("http://localhost:8000/log_mood", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
          user_id: "test1",
          mood: mood,
          date: date,
          journal_text: journal
      })
  })
  .then(res => res.json())
  .then(data => {
      document.getElementById("logResult").innerText = "Mood Saved!";
      loadDailySummary();
      loadWeeklySummary();
  })
  .catch(err => console.error(err));
}


// -----------------------------
// DAILY SUMMARY (GET) — Summary Service port 8001
// -----------------------------
function loadDailySummary() {
  const today = new Date().toISOString().split("T")[0];

  fetch(`http://localhost:8001/daily_summary?user_id=test1&date=${today}`)
      .then(res => res.json())
      .then(data => {
          document.getElementById("dailySummary").innerText =
              `Today's Summary:\nEntries: ${data.entries_today}\nAverage Mood: ${data.average_today}`;
      })
      .catch(err => console.error(err));
}


// -----------------------------
// WEEKLY SUMMARY (GET) — Summary Service port 8001
// -----------------------------
function loadWeeklySummary() {
  fetch(`http://localhost:8001/weekly_summary?user_id=test1`)
      .then(res => res.json())
      .then(data => {
          document.getElementById("weeklySummary").innerText =
              `Weekly Summary:\nEntries: ${data.entries_week}\nAverage Mood: ${data.weekly_average}`;
      })
      .catch(err => console.error(err));
}


// -----------------------------
// MOOD TREND (GET) — Trend Service port 8002
// -----------------------------
function loadTrend() {
  fetch("http://localhost:8002/trend?user_id=test1")
      .then(res => res.json())
      .then(data => {
          document.getElementById("trendResult").innerText =
              `Mood Trend: ${data.trend}`;
      })
      .catch(err => console.error(err));
}


// -----------------------------
// RECOMMENDATIONS (POST) — Recommendation Service port 8003
// -----------------------------
function getRecommendations(score) {
  fetch("http://localhost:8003/recommendations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mood_score: score })
  })
  .then(res => res.json())
  .then(data => {
      const chatBox = document.getElementById("chatBox");

      const botDiv = document.createElement("div");
      botDiv.classList.add("bot-bubble");
      botDiv.innerHTML = `
          <strong>Recommendations:</strong><br>
          ${data.coping_strategies.join("<br>")}
          ${data.osu_resources ? "<br><strong>Resources:</strong><br>" + data.osu_resources.join("<br>") : ""}
      `;

      chatBox.appendChild(botDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
  })
  .catch(err => console.error(err));
}
