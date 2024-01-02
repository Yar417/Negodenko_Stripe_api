
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe
  const stripe = window.Stripe(data.publicKey);

  document.querySelector("#submitBtnUSD").addEventListener("click", () => {
    startCheckout('usd');
  });

  document.querySelector("#submitBtnEUR").addEventListener("click", () => {
    startCheckout('eur');
  });

  function startCheckout(currency) {
    let selectedItems = [];
    let checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
    for (let i = 0; i < checkboxes.length; i++) {
        selectedItems.push(checkboxes[i].name);
    }

    // Get Checkout Session ID
    fetch('/create-order-checkout-session/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "items": selectedItems,
            "currency": currency,
        }),
    })
    .then((result) => { return result.json(); })
    .then((data) => {

      // Redirect to Stripe
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  }
});
