// ==============================
// Frontend entry point
// ==============================
// Import React root rendering utilities and global styles.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import "./styles/main.css";

// Mount the React application into the HTML root element.
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
