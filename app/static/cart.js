const cartContainer = document.getElementById("cartItems");
const totalSpan = document.getElementById("cartTotal");
const token = localStorage.getItem("token");

function loadCart() {
  fetch(`/cart/`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      cartContainer.innerHTML = "";
      totalSpan.innerText = data.total;

      data.items.forEach((item) => {
        cartContainer.innerHTML += `
          <div class="flex justify-between items-center border p-4 rounded-lg">
            <div class="w-[50%]">
              <h3 class="font-semibold text-gray-700">${item.name}</h3>
              <p class="text-gray-600 font-mono">$${item.price} x ${item.quantity}</p>
            </div>

            <div>
              <img src="${item.image_url}" alt="${item.name}" class="w-24 h-24 object-cover rounded">
            </div>

            <div class="flex items-center space-x-2">
              <button onclick="updateQty(${item.product_id}, ${item.quantity - 1})" class="px-2 bg-gray-200 rounded">-</button>
              <span class="w-4 text-center">${item.quantity}</span>
              <button onclick="updateQty(${item.product_id}, ${item.quantity + 1})" class="px-2 bg-gray-200 rounded">+</button>
              <button onclick="removeItem(${item.product_id})" class="text-red-500 hover:text-red-600 duration-300"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="m9.75 9.75 4.5 4.5m0-4.5-4.5 4.5M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
</svg>
</button>
            </div>
          </div>
        `;
      });
    });
}

function updateQty(productId, quantity) {
  fetch("/cart/update", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: quantity,
    }),
  }).then(() => loadCart());
}

function removeItem(productId) {
  fetch("/cart/update", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      product_id: productId,
      quantity: 0,
    }),
  }).then(() => loadCart());
}

loadCart();
