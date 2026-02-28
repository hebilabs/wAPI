const cartContainer = document.getElementById("cartItems");
const totalSpan = document.getElementById("cartTotal");
const token = localStorage.getItem("token");

/**
 * Load cart items from the server and render them
 * @returns
 */
async function loadCart() {
  try {
    const res = await fetch("/cart/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.status === 401) {
      window.location.href = "/login";
      return;
    }

    if (!res.ok) {
      throw new Error(`HTTP error ${res.status}`);
    }

    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error("Invalid JSON response");
    }

    if (!data || !Array.isArray(data.items)) {
      throw new Error("Invalid cart structure");
    }

    totalSpan.innerText = data.total ?? 0;

    let html = "";

    data.items.forEach((item) => {
      if (
        !item ||
        typeof item.product_id === "undefined" ||
        typeof item.quantity !== "number"
      ) {
        return;
      }

      const itemSubtotal = item.price * item.quantity;
      const originalSubtotal = item.price * 2 * item.quantity;

      html += `
  <div class="flex items-start gap-4 py-6 border-b border-zinc-100 group">
    <div class="w-24 h-32 flex-shrink-0 bg-zinc-100 overflow-hidden">
      <img src="${item.image_url}" alt="${item.name}" class="w-full h-full object-cover grayscale-[20%] group-hover:grayscale-0 transition-all duration-500">
    </div>

    <div class="flex-1 flex flex-col justify-between h-32">
      <div class="flex justify-between items-start">
        <div>
          <h3 class="text-xs font-black uppercase tracking-widest text-zinc-900">${item.name}</h3>
          <p class="text-[10px] text-zinc-400 uppercase mt-1 tracking-tighter">Unit: $${item.price}</p>
        </div>
        
        <button onclick="removeItem(${item.product_id})" class="text-zinc-300 hover:text-red-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="size-4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="flex justify-between items-end">
        <div class="flex items-center border border-zinc-200 bg-white">
          <button onclick="updateQty(${item.product_id}, ${item.quantity - 1})" 
                  class="px-3 py-1 text-zinc-500 hover:bg-zinc-100 transition-colors text-sm font-bold">-</button>
          <span class="px-3 py-1 text-[11px] font-black border-x border-zinc-200 min-w-[35px] text-center">${item.quantity}</span>
          <button onclick="updateQty(${item.product_id}, ${item.quantity + 1})" 
                  class="px-3 py-1 text-zinc-500 hover:bg-zinc-100 transition-colors text-sm font-bold">+</button>
        </div>

        <div class="text-right">
          <p class="text-[10px] text-zinc-400 uppercase tracking-widest mb-1">Subtotal</p>
          <p class="text-xs text-zinc-300 line-through font-mono leading-none">$${originalSubtotal}</p>
          <p class="text-base font-black text-black font-mono leading-none mt-1">$${itemSubtotal}</p>
        </div>
      </div>
    </div>
  </div>
`;
    });

    cartContainer.innerHTML = html;
  } catch (error) {
    console.error("Cart load error:", error);

    cartContainer.innerHTML = `
      <div class="text-red-500 p-4 border rounded">
        Error loading cart. Please try again.
      </div>
    `;
  }
}

/**
 * Update the quantity of a cart item on the server
 * @param {*} productId
 * @param {*} quantity
 */
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

/**
 * Remove the cart item setting the quantity to 0, smart right? :)
 * @param {*} productId
 */
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

function checkout() {
  window.location.href = "/checkout";
}
