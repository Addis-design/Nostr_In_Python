const socket = io();

const messageForm = document.getElementById('message-form');
const recipientSelect = document.getElementById('recipient-select');
const messageInput = document.getElementById('message');
const messageContainer = document.getElementById('message-container');

// Event listener for form submission
messageForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent form submission and page refresh

  const recipient = recipientSelect.value;
  const message = messageInput.value.trim();

  if (message) {
    // Create a Nostr event with the message content
    const event = {
      content: message,
      kind: 1, // Replace with the appropriate kind for your use case
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['p', recipient] // Replace with the appropriate tags for your use case
      ],
      pubkey: 'your_public_key', // Replace with the user's public key
    };

    // Sign the event with the user's private key
    const signedEvent = signEvent(event, 'your_private_key'); // Replace with the user's private key

    // Send the signed event to the server
    socket.emit('message', JSON.stringify(signedEvent));

    // Clear the message input field
    messageInput.value = '';
  }
});

// Handle incoming messages from the server
socket.on('message', (data) => {
  const event = JSON.parse(data);

  // Verify the event signature
  if (verifySignature(event)) {
    const messageElement = document.createElement('div');
    messageElement.textContent = `From: ${event.pubkey} | ${event.content}`;
    messageContainer.appendChild(messageElement);
  } else {
    console.log('Invalid event signature');
  }
});

// Function to sign an event with a private key (replace with your implementation)
function signEvent(event, privateKey) {
  // Your implementation for signing the event with the private key
  return event;
}

// Function to verify an event signature (replace with your implementation)
function verifySignature(event) {
  // Your implementation for verifying the event signature
  return true;
}