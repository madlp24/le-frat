console.log("stripe_elements.js loaded");

const publicKey = JSON.parse(
  document.getElementById("id_stripe_public_key").textContent
);
const clientSecret = JSON.parse(
  document.getElementById("id_client_secret").textContent
);

const stripe = Stripe(publicKey);
const elements = stripe.elements();

const card = elements.create("card", {
  hidePostalCode: true,
});
card.mount("#card-element");

const form = document.getElementById("payment-form");
const submitBtn = document.getElementById("submit-button");
const errorDiv = document.getElementById("card-errors");

// Spinner elements (added in checkout.html below)
const spinner = document.getElementById("submit-spinner");
const btnText = document.getElementById("submit-button-text");

function setLoading(isLoading) {
  if (!spinner || !btnText) return;

  if (isLoading) {
    submitBtn.disabled = true;
    spinner.classList.remove("d-none");
    btnText.textContent = "Processing…";
  } else {
    submitBtn.disabled = false;
    spinner.classList.add("d-none");
    btnText.textContent = "Pay now";
  }
}

card.on("change", (event) => {
  errorDiv.textContent = event.error ? event.error.message : "";
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  errorDiv.textContent = "";
  setLoading(true);

  try {
    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: { card: card },
    });

    if (result.error) {
      // Stripe validation/decline error
      errorDiv.textContent = result.error.message || "Payment failed. Please try again.";
      setLoading(false);
      return;
    }

    if (!result.paymentIntent) {
      errorDiv.textContent = "Payment could not be verified. Please try again.";
      setLoading(false);
      return;
    }

    if (result.paymentIntent.status === "succeeded") {
      const hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "payment_intent_id";
      hiddenInput.value = result.paymentIntent.id;
      form.appendChild(hiddenInput);

      // Keep loading state while the server processes the order
      form.submit();
      return;
    }

    // Any other status
    errorDiv.textContent = `Payment status: ${result.paymentIntent.status}. Please try again.`;
    setLoading(false);

  } catch (err) {
    // Network / unexpected error
    errorDiv.textContent = "Connection problem. Please refresh and try again.";
    setLoading(false);
  }
});

const statusHint = document.getElementById("payment-status-hint");

function setLoading(isLoading) {
  if (isLoading) {
    submitBtn.disabled = true;
    spinner.classList.remove("d-none");
    btnText.textContent = "Processing…";
    statusHint.textContent = "Do not refresh. Processing payment…";
  } else {
    submitBtn.disabled = false;
    spinner.classList.add("d-none");
    btnText.textContent = "Pay now";
    statusHint.textContent = "";
  }
}
