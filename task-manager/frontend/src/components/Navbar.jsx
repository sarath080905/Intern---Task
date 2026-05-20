// ==============================
// Navigation bar component
// ==============================
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { logout } = useAuth();

  return (
    <header className="navbar">
      <h2>Task Manager</h2>
      <nav>
        {/* Link to the protected dashboard page. */}
        <Link to="/dashboard">Dashboard</Link>
        <button onClick={logout} className="btn btn-danger" type="button">
          Logout
        </button>
      </nav>
    </header>
  );
}

export default Navbar;
