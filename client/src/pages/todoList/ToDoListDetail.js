import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import ToDoItem from "./ToDoItem";
import "../../index.css";

function ToDoListDetail() {
  const { id } = useParams();
  const [list, setList] = useState({
    id: 0,
    description: "",
    created_at: "",
    items: [],
    users: [],
  });
  const [inputText, setInputText] = useState("");

  console.log(list);

  useEffect(() => {
    fetch(`/todolists/${id}`)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => setList(data))
      .catch((error) => {
        console.error("Error fetching data: ", error);
      });
  }, [id]);

  function handleChange(e) {
    const newInput = e.target.value;
    setInputText(newInput);
  }

  function addItem(e) {
    e.preventDefault();
    if (inputText !== "") {
      fetch(`/todos`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: inputText,
          list_id: parseInt(id),
        }),
      })
        .then((r) => r.json())
        .then((data) => {
          setList((prevList) => ({
            ...prevList,
            items: [...prevList.items, data],
          }));
        })
        .then(setInputText(""));
    }
  }

  function deleteItem(tdId) {
    fetch(`/todos/${tdId}`, {
      method: "DELETE",
    });
    let updatedToDoData = list.items.filter((todo) => {
      return todo.id !== tdId;
    });
    setList((prevList) => ({
      ...prevList,
      items: [...updatedToDoData],
    }));
  }

  function updateCompleteStatus(tdId, status) {
    let result = list.items.map((td) => {
      if (td.id !== tdId) {
        return td;
      } else {
        return {
          ...td,
          completed: status,
        };
      }
    });
    setList((prevList) => ({
      ...prevList,
      items: [...result],
    }));
  }

  function editItem(tdId, status) {
    let tdCompletedPatch = !status;

    fetch(`/todos/${tdId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        completed: tdCompletedPatch,
      }),
    }).then(() => {
      updateCompleteStatus(tdId, tdCompletedPatch);
    });
  }

  const listOwners = list.users.map((user) => {
    return (
      <li key={user.id}>
        {user.name} | {user.email}
      </li>
    );
  });

  const renderedToDos = list.items.map((td) => {
    return (
      <ToDoItem key={td.id} todo={td} onDelete={deleteItem} onEdit={editItem} />
    );
  });

  return (
    <div className="list-div">
      <h2>{list.description}</h2>
      <h4>created: {list.created_at}</h4>
      <hr></hr>
      <h1>Friendly Pears & Collaborators:</h1>
      <ul>{listOwners}</ul>
      <hr></hr>

      <div className="list-card">
        {renderedToDos}
        <input onChange={handleChange} type="text" value={inputText} />
        <button onClick={addItem}>
          <span>Add</span>
        </button>
      </div>
    </div>
  );
}

export default ToDoListDetail;
