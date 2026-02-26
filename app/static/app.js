const token = localStorage.getItem("token");

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
       
                <div class="group relative flex flex-col bg-white transition-all duration-500">
  <div class="relative overflow-hidden bg-zinc-100 h-[450px]">
    <span class="absolute top-4 left-4 z-10 bg-black text-white text-[9px] font-bold px-2 py-1 uppercase tracking-widest">
      New Arrival
    </span>
    
     <div class="group cursor-pointer" onclick="window.location.href='/product/${p.id}'">
    <img 
      src="${p.image_url}" 
      alt="${p.name}" 
      class="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-110"
    >
    </div>

    <button 
      class="add-to-cart absolute bottom-0 w-full bg-black/90 text-white py-4 text-xs font-bold uppercase tracking-[0.2em] translate-y-full group-hover:translate-y-0 transition-transform duration-300 backdrop-blur-sm"
      data-id="${p.id}"
    >
      Add to bag +
    </button>
  </div>

  <div class="pt-4 pb-6 flex flex-col space-y-1">
    <div class="flex justify-between items-start">
      <div class="flex flex-col">
        <span class="text-[10px] text-zinc-400 uppercase tracking-widest font-medium">Essentials</span>
        <h3 class="text-sm font-bold text-zinc-900 uppercase tracking-tight truncate max-w-[180px]">
          ${p.name}
        </h3>
      </div>
      
      <p class="text-sm font-black text-zinc-900">
        $${p.price}
      </p>
    </div>

    <div class="flex gap-1.5 mt-2">
      <div class="w-3 h-3 rounded-full bg-black border border-zinc-200"></div>
      <div class="w-3 h-3 rounded-full bg-zinc-400 border border-zinc-200"></div>
      <div class="w-3 h-3 rounded-full bg-zinc-200 border border-zinc-200"></div>
    </div>
  </div>
</div>
                `;
      });
    });
}

function showCartToast(productName, imageUrl) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "fixed bottom-5 right-5 z-[100] flex flex-col gap-3";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `
        flex items-center w-80 bg-black text-white p-4 shadow-2xl transform translate-x-full 
        transition-all duration-500 ease-out border-l-4 border-red-600 backdrop-blur-md bg-opacity-90
    `;

  toast.innerHTML = `
        <img src="${imageUrl}" class="w-12 h-12 object-cover mr-4 border border-zinc-800">
        <div class="flex-1">
            <p class="text-[10px] uppercase tracking-widest text-zinc-400 font-bold">Added to Bag</p>
            <p class="text-xs font-bold truncate uppercase tracking-tighter">${productName}</p>
        </div>
        <button class="ml-4 text-zinc-500 hover:text-white">&times;</button>
    `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove("translate-x-full");
  }, 10);

  const removeToast = () => {
    toast.classList.add("opacity-0", "translate-y-2");
    setTimeout(() => toast.remove(), 500);
  };

  setTimeout(removeToast, 4000);
  toast.querySelector("button").onclick = removeToast;
}

document.addEventListener("click", async function (e) {
  if (e.target.closest(".add-to-cart")) {
    const button = e.target.closest(".add-to-cart");
    const productId = button.dataset.id;
    const imageUrl =
      button.parentElement.parentElement.querySelector("img").src;

    const response = await fetch("/cart/add", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_id: parseInt(productId),
        image_url: imageUrl,
      }),
    });

    if (response.ok) {
      showCartToast(productName, imageUrl);
    }
    if (response.status === 401) {
      window.location.href = "/login";
      return;
    }
  }
});
