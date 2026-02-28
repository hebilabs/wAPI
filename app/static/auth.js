const emailLoginInput = document.getElementById("login-email");
const passwordLoginInput = document.getElementById("login-password");
const loginForm = document.getElementById("loginForm");
const loginBtn = document.getElementById("loginBtn");

const registerForm = document.getElementById("registerForm");
const nameRegisterInput = document.getElementById("register-name");
const emailRegisterInput = document.getElementById("register-email");
const passwordRegisterInput = document.getElementById("register-password");
const addressRegisterInput = document.getElementById("register-address");
const acceptedTerms = document.getElementById("terms");
const registerBtn = document.getElementById("registerBtn");

const emailError = document.getElementById("emailError");
const passwordError = document.getElementById("passwordError");
const loginError = document.getElementById("loginError");
const registerError = document.getElementById("registerError");

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

/**
 * Auxiliary functions to validate
 * @param {} emailInput
 * @returns
 */

function validateEmail(emailInput) {
  if (!emailRegex.test(emailInput.value)) {
    emailError.textContent = "Enter a valid email address.";
    emailError.classList.remove("hidden");
    return false;
  }
  emailError.classList.add("hidden");
  return true;
}
function validatePassword(passwordInput) {
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

if (emailLoginInput) emailLoginInput.addEventListener("input", validateEmail);
if (passwordLoginInput)
  passwordLoginInput.addEventListener("input", validatePassword);

if (loginForm)
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const validEmail = validateEmail(emailLoginInput);
    const validPassword = validatePassword(passwordLoginInput);

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
          email: emailLoginInput.value,
          password: passwordLoginInput.value,
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

/**
 * Register functionality
 */
if (emailRegisterInput)
  emailRegisterInput.addEventListener("input", validateEmail);
if (passwordRegisterInput)
  passwordRegisterInput.addEventListener("input", validatePassword);

if (registerForm) {
  if (acceptedTerms) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const validEmail = validateEmail(emailRegisterInput);
      const validPassword = validatePassword(passwordRegisterInput);

      if (!validEmail || !validPassword) return;

      registerBtn.disabled = true;
      registerBtn.textContent = "Creating your account...";

      try {
        const res = await fetch("/users", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fullname: nameRegisterInput.value.trim(),
            email: emailRegisterInput.value.trim(),
            password: passwordRegisterInput.value,
            address: addressRegisterInput.value.trim(),
          }),
        });

        const data = await res.json().catch(() => null);

        if (!res.ok) {
          let message = "User could not be created.";

          if (res.status === 400) {
            message = data?.detail || "Invalid registration data.";
          }

          if (res.status === 409) {
            message = "Email already registered.";
          }

          if (res.status >= 500) {
            message = "Server error. Please try again later.";
          }

          throw new Error(message);
        }

        ToastManager.show({
          type: "success",
          content:
            '<span class="text-[10px] font-bold uppercase tracking-widest leading-none">Account created successfully</span>',
          duration: 3000,
        });
        registerForm.reset();
        window.location.href = "/login";
      } catch (err) {
        const message = err.message || "Network error. Please try again.";
        ToastManager.show({
          type: "error",
          content: `<span class="text-[10px] font-bold uppercase tracking-widest leading-none">${message}</span>`,
          duration: 3000,
        });
      } finally {
        registerBtn.disabled = false;
        registerBtn.textContent = "Register";
      }
    });
  } else {
    registerError.textContent = "You need to accept the terms and conditions.";
    registerError.classList.remove("hidden");
  }
}
