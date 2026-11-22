const API_URL = window.API_URL || "http://127.0.0.1:8000";
let currentConvId = null;

// 초기 데이터 불러오기
window.addEventListener("DOMContentLoaded", () => {
  loadSummary();
  loadDataList();
  loadConversations();
});

// 1. 데이터 요약 불러오기
async function loadSummary() {
  const box = document.getElementById("summary-content");
  try {
    const res = await fetch(`${API_URL}/api/data/summary`);
    const data = await res.json();
    box.innerHTML = `
      <b>기간:</b> ${data.period} (총 ${data.count}개)<br>
      <b>평균:</b> ${data.average}분 | <b>최대:</b> ${data.max}분 | <b>최소:</b> ${data.min}분<br>
      <b>최근 추세:</b> ${data.trend}
    `;
  } catch (err) {
    box.textContent = "요약 정보를 불러오지 못했습니다. (서버 깨어나는 중일 수 있음)";
  }
}

// 2. 데이터 목록 조회 (READ)
async function loadDataList() {
  const list = document.getElementById("data-list");
  list.innerHTML = "<li>불러오는 중...</li>";
  try {
    const res = await fetch(`${API_URL}/api/data`);
    const items = await res.json();
    list.innerHTML = "";
    items.slice(0, 30).forEach(item => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span><b>${item.date}</b> (${item.value}분)<br><small>${item.memo || ""}</small></span>
        <button class="delete-btn" onclick="deleteData('${item.id}')">삭제</button>
      `;
      list.appendChild(li);
    });
  } catch (err) {
    list.innerHTML = "<li>목록 조회 실패</li>";
  }
}

// 3. 데이터 추가 (CREATE)
document.getElementById("data-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    date: document.getElementById("data-date").value,
    value: Number(document.getElementById("data-value").value),
    memo: document.getElementById("data-memo").value
  };
  await fetch(`${API_URL}/api/data`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  e.target.reset();
  loadSummary();
  loadDataList();
});

// 4. 데이터 삭제 (DELETE)
async function deleteData(id) {
  if (!confirm("이 데이터를 삭제할까요?")) return;
  await fetch(`${API_URL}/api/data/${id}`, { method: "DELETE" });
  loadSummary();
  loadDataList();
}

// 5. 대화 기록 목록 불러오기
async function loadConversations() {
  const list = document.getElementById("conversation-list");
  try {
    const res = await fetch(`${API_URL}/api/conversations`);
    const convs = await res.json();
    list.innerHTML = "";
    convs.forEach(c => {
      const li = document.createElement("li");
      const titleSpan = document.createElement("span");
      titleSpan.textContent = c.title || "제목 없음";
      titleSpan.onclick = () => loadConversationDetail(c.id);

      const delBtn = document.createElement("button");
      delBtn.className = "delete-btn";
      delBtn.textContent = "삭제";
      delBtn.onclick = (e) => { e.stopPropagation(); deleteConversation(c.id); };

      li.appendChild(titleSpan);
      li.appendChild(delBtn);
      list.appendChild(li);
    });
  } catch (err) {
    list.innerHTML = "<li>기록 조회 실패</li>";
  }
}

// 6. 특정 대화 불러오기
async function loadConversationDetail(convId) {
  currentConvId = convId;
  const res = await fetch(`${API_URL}/api/conversations/${convId}`);
  const data = await res.json();
  const chatBox = document.getElementById("chat-box");
  chatBox.innerHTML = "";
  (data.messages || []).forEach(m => appendMessage(m.role, m.content));
}

// 7. 대화 삭제
async function deleteConversation(convId) {
  await fetch(`${API_URL}/api/conversations/${convId}`, { method: "DELETE" });
  if (currentConvId === convId) startNewChat();
  loadConversations();
}

// 새 대화 시작
function startNewChat() {
  currentConvId = null;
  document.getElementById("chat-box").innerHTML =
    `<div class="msg assistant">새 대화를 시작합니다. 무엇이든 물어보세요!</div>`;
}
document.getElementById("new-chat-btn").addEventListener("click", startNewChat);

// 8. AI 채팅 전송
document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";
  document.getElementById("loading").classList.remove("hidden");

  try {
    const res = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, conversation_id: currentConvId })
    });
    const data = await res.json();
    currentConvId = data.conversation_id;
    appendMessage("assistant", data.reply);
    loadConversations();
  } catch (err) {
    appendMessage("assistant", "오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
});

function appendMessage(role, text) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}