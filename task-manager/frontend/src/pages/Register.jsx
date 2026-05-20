// ==============================
// Register page
// ==============================
// Allow new users to create an account using email and password.
import { useState } from "react";
import { Link } from "react-router-dom";
import API from "../api/axios";
import "./register.css";

function Register() {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      // Backend currently accepts only email + password.
      await API.post("/register", {
        email: formData.email,
        password: formData.password,
      });
      setSuccess("Account created successfully. You can login now.");
      setFormData({ username: "", email: "", password: "" });
    } catch (err) {
      if (!err.response) {
        setError("Cannot reach backend server. Start FastAPI on port 8000.");
        return;
      }
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map((item) => item.msg).join(", "));
      } else {
        setError(detail || "Registration failed");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Creating account..." : "Register"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}
      <p className="auth-switch">
        Already have an account? <Link to="/">Login</Link>
      </p>
    </div>
  );
}

export default Register;
