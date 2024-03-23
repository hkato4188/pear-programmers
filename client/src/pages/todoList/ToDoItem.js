import React from "react";
import "../../index.css";

function ToDoItem({ ...props }) {
  const { todo, onDelete, onEdit } = props;
  const { completed, description, id } = todo;

  return (
    <>
      <div className="inline">
        <h4 className={completed ? "strikethrough" : "null"}>
          <span className="memo">📌 </span>
          {description}
        </h4>
      </div>
      <div>
        <button
          className="todo-button"
          onClick={() => {
            onEdit(id, completed);
          }}
        >
          Complete:<span>☑️</span>
        </button>
        <button
          className="todo-button"
          onClick={() => {
            onDelete(id);
          }}
        >
          Delete: <span>🗑️</span>
        </button>
      </div>
    </>
  );
}

export default ToDoItem;
