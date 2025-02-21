document.addEventListener("DOMContentLoaded", () => {
  const sendMessageButton = document.getElementById("sendMessage");
  const messageBox = document.getElementById("messageBox");
  const chatMessages = document.querySelector(".chat-messages");
  const chatTitle = document.querySelector(".chat-title span");
  const chatItems = document.querySelectorAll(".chat-item");

  // Function to send a message
  function sendMessage() {
    const messageText = messageBox.value.trim();
    if (messageText !== "") {
      // Add user message
      const userMessage = document.createElement("div");
      userMessage.classList.add("message", "sent");
      userMessage.textContent = messageText;
      chatMessages.appendChild(userMessage);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      // Auto-reply if user types "hi"
      if (messageText.toLowerCase() === "hi") {
        setTimeout(() => {
          const replyMessage = document.createElement("div");
          replyMessage.classList.add("message", "received");
          replyMessage.textContent = "Hello! How are you?";
          chatMessages.appendChild(replyMessage);
          chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
      }

      // Clear input box
      messageBox.value = "";
    }
  }

  


  // Click event for Send Button
  sendMessageButton.addEventListener("click", sendMessage);

  // Press "Enter" to send a message
  messageBox.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });

  // Load new chat when clicking on a chat or forum
  chatItems.forEach((item) => {
    item.addEventListener("click", () => {
      const newChatName = item.textContent; // Get chat/forum name
      chatTitle.textContent = `👤 ${newChatName}`; // Change chat title
      chatMessages.innerHTML = ""; // Clear previous chat

      // Add default received message
      const receivedMessage = document.createElement("div");
      receivedMessage.classList.add("message", "received");
      receivedMessage.textContent = "Hello! How can I help you?";
      chatMessages.appendChild(receivedMessage);
    });
  });

  // Video Call Alert
  document.getElementById("videoCall").addEventListener("click", () => {
    const receivedMessage = document.createElement("div");
      receivedMessage.classList.add("message", "received");
      receivedMessage.textContent = "Join the video call: https://meet.google.com/dat-nqwq-qob";
      chatMessages.appendChild(receivedMessage);
  });

});

