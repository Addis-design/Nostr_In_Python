const message = document.getElementById("messages");
const recipientInput = document.getElementById("recipient-input");

message.addEventListener("click", function (event) {
  recipientInput.value = event.target.innerText;
});

document.addEventListener("DOMContentLoaded", function () {
  const recipientInput = document.getElementById("recipient-input");

  // Add event listener to the document, delegating the click event to all messages
  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("message")) {
      recipientInput.value = event.target.innerText;
    }
  });
});
document.addEventListener("DOMContentLoaded", function () {
  const sendButton = document.getElementById("send-button");
  const alert = document.getElementById("alert");

  sendButton.addEventListener("click", function () {
    alert.textContent = "Sent";
    alert.classList.add("alert-success");
    alert.style.display = "block";
  });
});
