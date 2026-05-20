// ==============================
// Dashboard page
// ==============================
// Show tasks, create new tasks, and manage task state.
import { useEffect, useMemo, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";
import TaskCard from "../components/TaskCard";
import { useAuth } from "../context/AuthContext";
import "./Dashboard.css"; 

function Dashboard() {
  const { logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Calculate completed tasks for UI stats.
  const completedCount = useMemo(
    () => tasks.filter((task) => task.completed).length,
    [tasks],
  );

  const loadTasks = async () => {
    setLoading(true);
    setError("");

    try {
      const { data } = await API.get("/tasks", {
        params: { page: 1, limit: 100 },
      });
      setTasks(data.items || []);
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        return;
      }
      setError(err.response?.data?.detail || "Could not fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks when the component loads.
  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    setError("");
    setSaving(true);

    try {
      await API.post("/tasks", {
        title: title.trim(),
        description: description.trim() || null,
      });
      setTitle("");
      setDescription("");
      await loadTasks();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not create task");
    } finally {
      setSaving(false);
    }
  };

  const handleToggleTask = async (task, completed) => {
    try {
      await API.put(`/tasks/${task.id}`, {
        title: task.title,
        description: task.description,
        completed,
      });
      loadTasks();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not update task");
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await API.delete(`/tasks/${taskId}`);
      setTasks((prev) => prev.filter((task) => task.id !== taskId));
    } catch (err) {
      setError(err.response?.data?.detail || "Could not delete task");
    }
  };

  return (
    <>
      <Navbar />
      <main className="dashboard">
        <section className="container">
          <h3>Create Task</h3>
          <form onSubmit={handleCreateTask}>
            <input
              type="text"
              placeholder="Task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <button type="submit" disabled={saving}>
              {saving ? "Adding..." : "Add Task"}
            </button>
          </form>

          <div className="stats">
            <span>Total: {tasks.length}</span>
            <span>Completed: {completedCount}</span>
          </div>

          {loading && <p>Loading tasks...</p>}
          {error && <p className="error">{error}</p>}
          {!loading && tasks.length === 0 && <p>No tasks found. Create your first task.</p>}

          <div className="task-grid">
            {tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onToggle={handleToggleTask}
                onDelete={handleDeleteTask}
              />
            ))}
          </div>
        </section>
      </main>
    </>
  );
}

export default Dashboard;
