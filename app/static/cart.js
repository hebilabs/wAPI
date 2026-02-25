const userId = 1;
const cartContainer = document.getElementById("cartItems");
const totalSpan = document.getElementById("cartTotal");

function loadCart() {
  fetch(`/cart/${userId}`)
    .then((res) => res.json())
    .then((data) => {
      cartContainer.innerHTML = "";
      totalSpan.innerText = data.total;

      data.items.forEach((item) => {
        cartContainer.innerHTML += `
          <div class="flex justify-between items-center border p-4 rounded">
            <div>
              <h3 class="font-semibold">${item.name}</h3>
              <p>$${item.price} x ${item.quantity}</p>
            </div>

            <div class="flex items-center space-x-2">
              <button onclick="updateQty(${item.product_id}, ${item.quantity - 1})" class="px-2 bg-gray-200">-</button>
              <span>${item.quantity}</span>
              <button onclick="updateQty(${item.product_id}, ${item.quantity + 1})" class="px-2 bg-gray-200">+</button>
              <button onclick="removeItem(${item.product_id})" class="px-2 bg-red-500 text-white">x</button>
            </div>
          </div>
        `;
      });
    });
}

function updateQty(productId, quantity) {
  fetch("/cart/update", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      quantity: quantity,
    }),
  }).then(() => loadCart());
}

function removeItem(productId) {
  fetch("/cart/remove", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      quantity: 0,
    }),
  }).then(() => loadCart());
}

loadCart();
