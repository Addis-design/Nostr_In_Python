const public_key = document.getElementById("public_key");
const public_key_input = document.getElementById("public_key_input");

public_key.addEventListener("click", function () {
  public_key_input.value = public_key.innerHTML;
  public_key_input.innerHTML = public_key.innerHTML;
});
