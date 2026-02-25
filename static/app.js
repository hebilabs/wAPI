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
                <div class="bg-gray-800 p-4 rounded">
                    <h3 class="text-xl">${p.name}</h3>
                    <p>${p.description}</p>
                    <p class="text-green-400">$${p.price}</p>
                </div>
                `;
      });
    });
}

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
