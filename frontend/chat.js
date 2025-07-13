document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('mb-2');
        div.textContent = text;
        if (sender === 'user') {
            div.classList.add('text-end');
        }
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        addMessage(message, 'user');
        userInput.value = '';
        try {
            const response = await fetch('http://127.0.0.1:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            addMessage(data.reply, 'bot');
        } catch (err) {
            addMessage('Error: ' + err.message, 'bot');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
