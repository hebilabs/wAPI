/**
 * Simple logout function to clear token
 */
function logout() {
  localStorage.removeItem("token");
  window.location.href = "/login";
}
