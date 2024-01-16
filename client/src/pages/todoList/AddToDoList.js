import React, { useContext, useState } from "react";
import { UserContext } from "../../context/user";
import { useHistory } from "react-router-dom";
import "../../index.css";

function AddToDoList() {
  const { user } = useContext(UserContext);
  const [listDescription, setListDescription] = useState("");
  const history = useHistory();

  function handleSubmit(e) {
    e.preventDefault();
    let new_list = {
      description: listDescription,
      user_id: user.id,
    };
    console.log(new_list);
    fetch("/todolists", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(new_list),
    })
      .then((r) => r.json())
      .then((data) => history.push(`/todolists/${data.id}`));
  }
  function handleChange(e) {
    setListDescription(() => e.target.value);
  }

  console.log(listDescription);
  return (
    <div className="group-card outline login-container">
      <div className="login-form">
        <h2>Add new list</h2>

        <form onSubmit={handleSubmit}>
          <div className="">
            <label className="list-header">Description: </label>
            <input
              className="list-input"
              name="description"
              type="text"
              placeholder="List Description"
              value={listDescription}
              onChange={handleChange}
            />
          </div>
          <br></br>
          <button className="toggle-button" type="submit">
            📝 Create 📝
          </button>
        </form>
      </div>
    </div>
  );
}

export default AddToDoList;
