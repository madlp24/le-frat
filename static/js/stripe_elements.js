console.log("stripe_elements.js loaded");

const publicKey = JSON.parse(
  document.getElementById("id_stripe_public_key").textContent
);
const clientSecret = JSON.parse(
  document.getElementById("id_client_secret").textContent
);

const stripe = Stripe(publicKey);
const elements = stripe.elements();
const card = elements.create("card");
card.mount("#card-element");

card.on("change", (event) => {
  const errorDiv = document.getElementById("card-errors");
  errorDiv.textContent = event.error ? event.error.message : "";
});

const form = document.getElementById("payment-form");
const submitBtn = document.getElementById("submit-button");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  submitBtn.disabled = true;

  const { error, paymentIntent } = await stripe.confirmCardPayment(
    clientSecret,
    { payment_method: { card: card } }
  );

  if (error) {
    document.getElementById("card-errors").textContent = error.message;
    submitBtn.disabled = false;
    return;
  }

  if (paymentIntent.status === "succeeded") {
    const hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.name = "payment_intent_id";
    hiddenInput.value = paymentIntent.id;
    form.appendChild(hiddenInput);
    form.submit();
  }
});
