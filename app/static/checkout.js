const token = localStorage.getItem("token");
const checkoutItems = document.getElementById("checkoutItems");
const subtotalSpan = document.getElementById("subtotal");
const finalTotalSpan = document.getElementById("finalTotal");
const checkoutForm = document.getElementById("checkoutForm");
const cardNumberInput = document.getElementById("cardNumber");
const cardDisplayNumber = document.getElementById("cardDisplayNumber");

async function checkAuth() {
  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch("/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
  } catch {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}

async function loadCheckoutCart() {
  if (!token) {
    window.location.href = "/login";
    return;
  }

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

    const data = await res.json();

    if (!data || !Array.isArray(data.items)) {
      throw new Error("Invalid cart structure");
    }

    let html = "";
    let subtotal = 0;

    data.items.forEach((item) => {
      if (
        !item ||
        typeof item.product_id === "undefined" ||
        typeof item.quantity !== "number"
      ) {
        return;
      }

      const itemSubtotal = item.price * item.quantity;
      subtotal += itemSubtotal;

      html += `
      <div class="flex gap-4">
        <div class="w-16 h-20 bg-zinc-200 flex-shrink-0 overflow-hidden">
          <img src="${item.image_url}" alt="${item.name}" class="w-full h-full object-cover">
        </div>
        <div class="flex-1 flex justify-between">
          <div>
            <p class="text-[10px] font-black uppercase">${item.name}</p>
            <p class="text-[9px] text-zinc-400 uppercase tracking-widest">
              Qty: ${item.quantity}
            </p>
          </div>
          <p class="text-[10px] font-bold font-mono">$${itemSubtotal.toFixed(2)}</p>
        </div>
      </div>
      `;
    });

    checkoutItems.innerHTML =
      html ||
      `<p class="text-[11px] text-zinc-400 uppercase tracking-widest">Your cart is empty.</p>`;

    subtotalSpan.innerText = subtotal.toFixed(2);
    finalTotalSpan.innerText = subtotal.toFixed(2);
  } catch (error) {
    console.error("Checkout cart load error:", error);
    checkoutItems.innerHTML = `
      <div class="text-red-500 p-4 border rounded">
        Error loading cart. Please try again.
      </div>
    `;
  }
}

function formatCardNumber(value) {
  return value
    .replace(/\D/g, "")
    .replace(/(.{4})/g, "$1 ")
    .trim()
    .slice(0, 19);
}

if (cardNumberInput && cardDisplayNumber) {
  cardNumberInput.addEventListener("input", (e) => {
    const formatted = formatCardNumber(e.target.value);
    e.target.value = formatted;
    cardDisplayNumber.textContent = formatted || "•••• •••• •••• ••••";
  });
}

if (checkoutForm) {
  checkoutForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!token) {
      window.location.href = "/login";
      return;
    }

    const code = (cardNumberInput?.value || "").trim();

    if (!code) {
      alert("Please enter a (fake) card number.");
      return;
    }

    try {
      const res = await fetch("/cart/checkout/payment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data || data.total_paid === 0) {
        ToastManager.show({
          type: "error",
          content: `<span class="text-[10px] font-bold uppercase tracking-widest leading-none">Payment failed. Please try again.</span>`,
          duration: 3000,
        });
        return;
      }
      ToastManager.show({
        type: "success",
        content: `<span class="text-[10px] font-bold uppercase tracking-widest leading-none">Payment authorized! Total paid: $${Number(
          data.total_paid ?? 0,
        ).toFixed(2)}</span>`,
        duration: 3000,
      });
      window.location.href = "/bag";
    } catch (error) {
      ToastManager.show({
        type: "error",
        content: `<span class="text-[10px] font-bold uppercase tracking-widest leading-none">Payment failed. Please try again.</span>`,
        duration: 3000,
      });
      console.error("Checkout error:", error);
    }
  });
}

checkAuth();
loadCheckoutCart();
