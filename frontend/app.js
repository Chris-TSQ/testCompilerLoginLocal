import { signup, login, logout } from "./api.js";

const loginView = document.getElementById("login-view");
const signupView = document.getElementById("signup-view");
const dashboardView = document.getElementById("dashboard-view");
const errorMessage = document.getElementById("error-message");

const showError = (msg) => {
  errorMessage.textContent = msg;
  errorMessage.style.display = "block";
};

const hideError = () => (errorMessage.style.display = "none");

const showView = (view) => {
  [loginView, signupView, dashboardView].forEach(
    (v) => (v.style.display = "none")
  );
  view.style.display = "block";
  hideError();
};

const showDashboard = (username) => {
  showView(dashboardView);
  document.getElementById("username").textContent = username;
};

document.getElementById("show-signup").onclick = () => showView(signupView);
document.getElementById("show-login").onclick = () => showView(loginView);

document.getElementById("signup-btn").onclick = async () => {
  const data = {
    username: signupUsername.value,
    email: signupEmail.value,
    password: signupPassword.value,
  };

  if (Object.values(data).some((v) => !v)) {
    return showError("All fields are required");
  }

  const res = await signup(data);
  res.ok ? showView(loginView) : showError(res.data.error);
};

document.getElementById("login-btn").onclick = async () => {
  const data = {
    username: loginUsername.value,
    password: loginPassword.value,
  };

  if (!data.username || !data.password) {
    return showError("Username and password are required");
  }

  const res = await login(data);
  if (res.ok) {
    localStorage.setItem("authToken", res.data.token);
    showDashboard(res.data.username);
  } else {
    showError(res.data.error);
  }
};

document.getElementById("logout-btn").onclick = async () => {
  await logout(localStorage.getItem("authToken"));
  localStorage.removeItem("authToken");
  showView(loginView);
};

showView(loginView);
