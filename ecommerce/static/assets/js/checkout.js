document.addEventListener('DOMContentLoaded', function() {
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const checkoutForm = document.getElementById('checkoutForm');
  const placeOrderBtn = document.getElementById('placeOrderBtn');
  const paymentMethodModal = new bootstrap.Modal(document.getElementById('paymentMethodModal'));

  // Cart Initialization and Display
  function updateCartDisplay() {
      const itemsContainer = $('#items');
      const totalPriceSpan = $('#totalprice');
      const itemsJsonInput = $('#itemsJson');
      const amtInput = $('#amt');

      itemsContainer.empty();
      let totalPrice = 0;

      if (Object.keys(cart).length === 0) {
          itemsContainer.append('<p>Your cart is empty. Please add items before checkout.</p>');
      } else {
          Object.entries(cart).forEach(([itemKey, itemDetails]) => {
              const [qty, name, price, imageUrl] = itemDetails;
               totalPrice += qty * price;
              itemsContainer.append(`
                  <li class="list-group-item d-flex justify-content-between align-items-center">
                      <div class="d-flex align-items-center">
                          <img src="${imageUrl}" alt="${name}" style="width: 50px; height: 50px; object-fit: cover; margin-right: 15px;">
                          <div>
                              <h6 class="mb-2">${name}</h6>
                              <div class="d-flex align-items-center">
                                  <button class="btn btn-md minus-item" data-item="${itemKey}">-</button>
                                  <span class="mx-2">${qty}</span>
                                  <button class="btn btn-md plus-item" data-item="${itemKey}">+</button>
                              </div>
                          </div>
                      </div>
                      <div>
                          <span class="text-muted">$${(price * qty).toFixed(2)}</span>
                      </div>
                  </li>
              `);
          });
      }

      totalPriceSpan.text(totalPrice.toFixed(2));
      itemsJsonInput.val(JSON.stringify(cart));
      amtInput.val(totalPrice);
  }

  // Event listeners for plus and minus buttons
  $(document).on('click', '.minus-item', function() {
      const itemKey = $(this).data('item');
      if (cart[itemKey]) {
          cart[itemKey][0]--;
          if (cart[itemKey][0] <= 0) {
              delete cart[itemKey];
          }
          updateCartDisplay();
      }
  });

  $(document).on('click', '.plus-item', function() {
      const itemKey = $(this).data('item');
      if (cart[itemKey]) {
          cart[itemKey][0]++;
          updateCartDisplay();
      }
  });

  // Form submission
  checkoutForm.addEventListener('submit', function(e) {
      e.preventDefault();
      if (this.checkValidity()) {
          const formData = new FormData(this);
          fetch('/checkout/', {
              method: 'POST',
              body: formData,
              headers: {
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  showPaymentOptions(data.midtrans_token);
              } else {
                  alert(`Error: ${data.message}`);
              }
          })
          .catch(error => {
              console.error('Error:', error);
              alert('An unexpected error occurred');
          });
      } else {
          alert('Please fill in all required fields');
      }
  });

  // Show payment options
  function showPaymentOptions(midtransToken) {
      const paymentMethods = `
          <button class="btn btn-primary" onclick="payWithMidtrans('${midtransToken}')">Pay with Midtrans</button>
      `;
      $('#paymentMethodContainer').html(paymentMethods);
      paymentMethodModal.show();
  }

  // Payment function
  window.payWithMidtrans = function(midtransToken) {
      snap.pay(midtransToken, {
          onSuccess: function(result) {
              alert('Payment successful!');
              window.location.href = '/order-success/';
          },
          onPending: function(result) {
              alert('Payment is pending');
          },
          onError: function(result) {
              alert('Payment failed');
          },
          onClose: function() {
              console.log('Payment modal closed');
          }
      });
  };

  // Initialize cart display
  updateCartDisplay();
});