const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const form = document.getElementById("loginForm");
const loginBtn = document.getElementById("loginBtn");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");
const loginError = document.getElementById("loginError");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

function validateEmail() {
  if (!emailRegex.test(emailInput.value)) {
    emailError.textContent = "Enter a valid email address.";
    emailError.classList.remove("hidden");
    return false;
  }
  emailError.classList.add("hidden");
  return true;
}

function validatePassword() {
  if (!passwordRegex.test(passwordInput.value)) {
    passwordError.textContent =
      "Password must be 8+ chars, include uppercase, lowercase and a number.";
    passwordError.classList.remove("hidden");
    return false;
  }
  passwordError.classList.add("hidden");
  return true;
}

/**
 * Handle form submission for login
 */

emailInput.addEventListener("input", validateEmail);
passwordInput.addEventListener("input", validatePassword);

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const validEmail = validateEmail();
  const validPassword = validatePassword();

  if (!validEmail || !validPassword) return;

  loginBtn.disabled = true;
  loginBtn.textContent = "Logging in...";

  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: emailInput.value,
        password: passwordInput.value,
      }),
    });

    const data = await res.json();

    if (data.access_token) {
      localStorage.setItem("token", data.access_token);
      window.location.href = "/shop";
    } else {
      throw new Error("Invalid credentials");
    }
  } catch (err) {
    loginError.textContent = "Invalid email or password.";
    loginError.classList.remove("hidden");
  } finally {
    loginBtn.disabled = false;
    loginBtn.textContent = "Login";
  }
});

/**
 * Checking if user is already authenticated
 */
async function checkAuth() {
  console.log("Entering");
  const token = localStorage.getItem("token");
  if (token) {
    try {
      const res = await fetch("/auth/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (res.ok) {
        const data = await res.json();
        window.location.href = `/profile/${data.user_id}`;
      } else {
        localStorage.removeItem("token");
        window.location.href = "/";
      }
    } catch {
      localStorage.removeItem("token");
      window.location.href = "/";
    }
  }
}

checkAuth();
