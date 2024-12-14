if (localStorage.getItem('cart') == null) {
var cart = {};
} else {
    var cart = JSON.parse(localStorage.getItem('cart'));
    updateCart(cart);
}

$('.divpr').on('click', 'button.cart', function() {
    var idstr = this.id.toString();
    if (cart[idstr] !== undefined) {
        qty = cart[idstr][0] + 1;
    } else {
        qty = 1;
        name = document.getElementById('namepr' + idstr.slice(2)).innerHTML;
        price = document.getElementById('pricepr' + idstr.slice(2)).innerHTML;

        var imageUrl = document.querySelector(`#pr${idstr.slice(2)}`).closest('.card').querySelector('.card-img-top').src;
        cart[idstr] = [qty, name, price, imageUrl];
    }
    updateCart(cart);
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = Object.keys(cart).length;
    console.log(Object.keys(cart).length);
    document.getElementById('popcart').click();
});

$('#popcart').popover();
updatePopover(cart);

function updatePopover(cart) {
    console.log('we are inside update popover');
    var popStr = "<h5>Cart for your items in my shopping cart</h5>";
    var i = 1;
    var totalItems = 0;

    if (Object.keys(cart).length === 0) {
        popStr += "<p>Your cart is empty</p>";
    } else {
        for (var item in cart) {
            var productName = document.getElementById('namepr' + item.slice(2)).innerHTML.slice(0, 19);
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

        $(document).on('click', '#clearCartBtn', function(e) {
            e.preventDefault();
            clearCart();
        });
    }

    document.getElementById('popcart').setAttribute('data-content', popStr);
    $('#popcart').popover('show');
    document.getElementById("popcart").click();
}

function clearCart() {
    cart = JSON.parse(localStorage.getItem('cart')) || {};

    for (var item in cart) {
        let productId = item.slice(2);
        
        let divElement = document.getElementById('divpr' + productId);
        if (divElement) {
            divElement.innerHTML = `<button id="pr${productId}" class="btn btn-danger cart btn-sm mt-0">Add To Cart</button>`;
        }
    }

    localStorage.removeItem('cart');
    cart = {};
    updateCart(cart);
    updatePopover(cart);
    $('#popcart').popover('hide');
    
    document.getElementById('cart').innerHTML = '0';
}

function updateCart(cart) {
    var sum = 0;
    for (var item in cart) {
        sum = sum + cart[item][0];
        document.getElementById('div' + item).innerHTML = 
            "<button id='minus" + item + "' class='btn btn-success minus'>-</button> " +
            "<span id='val" + item + "'>" + cart[item][0] + "</span> " +
            "<button id='plus" + item + "' class='btn btn-success plus'>+</button>";
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart').innerHTML = sum;
    console.log(cart);
    updatePopover(cart);
    document.getElementById("popcart").click();
}


$('.divpr').on("click", "button.minus", function() {
    a = this.id.slice(7);
    cart['pr' + a][0] = cart['pr' + a][0] - 1;
    if (cart['pr' + a][0] <= 0) {
        delete cart['pr' + a];
        document.getElementById('divpr' + a).innerHTML = 
            `<button id="pr${a}" class="btn btn-danger cart btn-sm mt-0">Add To Cart</button>`;
    } else {
        document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    }
    
    updateCart(cart);
});

$('.divpr').on("click", "button.plus", function() {
    a = this.id.slice(6);
    if (!cart['pr' + a]) {
        qty = 1;
        name = document.getElementById('namepr' + a).innerHTML;
        price = document.getElementById('pricepr' + a).innerHTML;
        cart['pr' + a] = [qty, name, price];
        
        document.getElementById('divpr' + a).innerHTML = 
            `<button id="minus${a}" class="btn btn-success minus">-</button> ` +
            `<span id="valpr${a}">1</span> ` +
            `<button id="plus${a}" class="btn btn-success plus">+</button>`;
    } else {
        cart['pr' + a][0] = cart['pr' + a][0] + 1;
        document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    }
    
    updateCart(cart);
});