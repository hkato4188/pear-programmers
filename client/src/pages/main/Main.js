import React, { useContext } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Login from "../login/LoginPage";
import About from "../about/About";
import ToDosPage from "../todoList/ToDosPage";
import ToDoListDetail from "../todoList/ToDoListDetail";
import AddToDoList from "../todoList/AddToDoList";
import { UserContext } from "../../context/user";

function Main() {
  const { user } = useContext(UserContext);

  return (
    <div>
      <NavBar />
      <div className="user-profile">
        <h4 className="username">{user.name} 💻 💬</h4>
      </div>
      <Switch>
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/">
          <About />
        </Route>
        <Route exact path="/todolists">
          <ToDosPage />
        </Route>
        <Route exact path="/todolists/:id">
          <ToDoListDetail />
        </Route>
        <Route exact path="/add_todolist">
          <AddToDoList />
        </Route>
      </Switch>
    </div>
  );
}

export default Main;
