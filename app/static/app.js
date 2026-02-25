const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);

    const response = await fetch("/auth/login", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    document.getElementById("loginResult").innerText = JSON.stringify(
      data,
      null,
      2,
    );
  });
}

const productList = document.getElementById("productList");
if (productList) {
  fetch("/products")
    .then((res) => res.json())
    .then((products) => {
      products.forEach((p) => {
        productList.innerHTML += `
                <div class= p-4 rounded">
                    <div>
                        <img src="${p.image_url}" alt="${p.name}" class="w-full h-96 object-cover rounded mb-4">
                    </div>
                    
                    <div class="flex flex-row items-center justify-between mt-2">
                      <h3 class="text-lg font-sans text-gray-700 w-[90%] truncate">${p.name}</h3>
                      <button class="text-gray-700 hover:text-red-500 add-to-cart" data-id="${p.id}"">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
</svg>

                      </button>
                      <div>
                      </div>
                    </div>
                      <p class="text-gray-600 font-mono">$${p.price}</p>
                </div>
                `;
      });
    });
}

document.addEventListener("click", function (e) {
  if (e.target.closest(".add-to-cart")) {
    const button = e.target.closest(".add-to-cart");
    const productId = button.dataset.id;

    fetch("/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        product_id: parseInt(productId),
        user_id: 1,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("Producto añadido al carrito 🛒");
      });
  }
});

// CART
const cartForm = document.getElementById("cartForm");
if (cartForm) {
  cartForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(cartForm));

    const response = await fetch("/cart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const result = await response.json();
    document.getElementById("cartResult").innerText = JSON.stringify(
      result,
      null,
      2,
    );
  });
}
