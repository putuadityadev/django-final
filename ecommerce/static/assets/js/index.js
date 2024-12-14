document.addEventListener('DOMContentLoaded', function() {
  // Inisialisasi cart dari localStorage
  var cart = localStorage.getItem('cart') ? JSON.parse(localStorage.getItem('cart')) : {};
  
  console.log('Existing cart:', cart);
  
  // Update cart badge dan popover
  updateCart(cart);

  // Event listener untuk tombol cart
  $('.divpr').on('click', 'button.cart', function() {
      var idstr = this.id.toString();

      if (cart[idstr] !== undefined) {
          cart[idstr][0] += 1;
      } else {
          var qty = 1;
          var name = document.getElementById('namepr' + idstr.slice(2)).innerHTML;
          var price = document.getElementById('pricepr' + idstr.slice(2)).innerHTML;
          cart[idstr] = [qty, name, price];
      }

      updateCart(cart);
  });

  function updateCart(cart) {
      var sum = 0;
      for (var item in cart) {
          sum += cart[item][0];
      }

      // Update cart badge
      var cartBadge = document.getElementById('cart');
      if (cartBadge) {
          cartBadge.innerHTML = sum;
      }

      // Simpan ke localStorage
      localStorage.setItem('cart', JSON.stringify(cart));

      // Update popover
      updatePopover(cart);
  }

  function updatePopover(cart) {
      var popStr = "<h5>Cart for your items in my shopping cart</h5>";
      var i = 1;
      var totalItems = 0;

      if (Object.keys(cart).length === 0) {
          popStr += "<p>Your cart is empty</p>";
      } else {
          for (var item in cart) {
              var productNameElement = document.getElementById('namepr' + item.slice(2));
              var productName = productNameElement ? productNameElement.innerHTML.slice(0, 19) : 'Unknown Product';
              
              popStr += "<b>" + i + "</b> " + productName + " Qty: " + cart[item][0] + "<br>";
              
              totalItems += cart[item][0];
              i++;
          }

          popStr += `
          <div class="cart-actions mt-2 d-flex justify-content-between">
              <a href='/checkout' class='btn btn-success btn-sm'>Checkout</a>
              <a href='#' id='clearCartBtn' class='btn btn-danger btn-sm'>Clear Cart</a>
          </div>
          `;
      }

      var popcartElement = document.getElementById('popcart');
      if (popcartElement) {
          popcartElement.setAttribute('data-content', popStr);
          $('#popcart').popover('show');
          popcartElement.click();
      }
  }

  // Event listener untuk clear cart
  $(document).on('click', '#clearCartBtn', function(e) {
      e.preventDefault();
      clearCart();
  });

  function clearCart() {
      // Reset cart
      cart = {};
      
      // Update localStorage
      localStorage.removeItem('cart');
      
      // Update cart
      updateCart(cart);
      
      // Sembunyikan popover
      $('#popcart').popover('hide');
  }

  // Event listener untuk tombol plus dan minus
  $('.divpr').on("click", "button.minus", function() {
      var a = this.id.slice(7);
      
      if (cart['pr' + a]) {
          cart['pr' + a][0] -= 1;
          
          if (cart['pr' + a][0] <= 0) {
              delete cart['pr' + a];
          }
          
          updateCart(cart);
      }
  });

  $('.divpr').on("click", "button.plus", function() {
      var a = this.id.slice(6);
      
      if (!cart['pr' + a]) {
          var qty = 1;
          var name = document.getElementById('namepr' + a).innerHTML;
          var price = document.getElementById('pricepr' + a).innerHTML;
          cart['pr' + a] = [qty, name, price];
      } else {
          cart['pr' + a][0] += 1;
      }
      
      updateCart(cart);
  });
});