// ==============================
// Task card component
// ==============================
// Display a single task and allow status toggling and deletion.
function TaskCard({ task, onToggle, onDelete }) {
  return (
    <div className={`task-card ${task.completed ? "completed" : ""}`}>
      <div className="task-content">
        <h4>{task.title}</h4>
        <p>{task.description || "No description"}</p>
      </div>

      <div className="task-actions">
        <label>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onToggle(task, e.target.checked)}
          />
          Done
        </label>
        <button className="btn btn-danger" onClick={() => onDelete(task.id)} type="button">
          Delete
        </button>
      </div>
    </div>
  );
}

export default TaskCard;
