import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../../context/user";
import "../../index.css";

function ToDoList({ ...props }) {
  const { user } = useContext(UserContext);
  const { tdlist, onDelete, onUpdateOwner } = props;
  const { id, description, items, users } = tdlist;

  const list_owners = users.map((u) => {
    return (
      <React.Fragment key={u.id}>
        {u.name} | {u.email}
        <br></br>
      </React.Fragment>
    );
  });

  const owner_ids = users.map((m) => m.id);
  const list_owner = owner_ids.includes(user.id);

  return (
    <div className={list_owner ? "list outline-highlight" : "list outline"}>
      <h2>{description}</h2>
      <h3>Owners:</h3>
      <div>{list_owners}</div>

      <h4>
        <span className="memo">🗒️</span> No. of items: {items.length}
      </h4>

      <div className="bottom">
        <button
          className="btn"
          onClick={() => onUpdateOwner(id, user.id, list_owner)}
        >
          {!list_owner ? "Join" : "Leave"}
        </button>

        {list_owner ? (
          <>
            <Link className="btn" to={`/todolists/${id}`}>
              Get to work
            </Link>
            <button className="btn" onClick={() => onDelete(id)}>
              Delete
            </button>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default ToDoList;
