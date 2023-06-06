const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');

function addUserMessage(message) {
  const messageDiv = document.createElement('div');
  messageDiv.className = 'user-message';
  messageDiv.textContent = message;
  chatLog.appendChild(messageDiv);
}

userInput.addEventListener('keyup', function(event) {
  if (event.keyCode === 13) {
    const message = userInput.value.trim();
    if (message !== '') {
      addUserMessage(message);
      userInput.value = '';
      // Handle bot response logic here...
    }
  }
});
