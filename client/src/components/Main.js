import React, { useContext } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import Login from "./Login";
import About from "./About";
import { UserContext } from "../context/user";

function Main() {
  const { user } = useContext(UserContext);

  return (
    <div>
      <NavBar />
      <h4>User: {user.name}</h4>
      <Switch>
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/">
          <About />
        </Route>
      </Switch>
    </div>
  );
}

export default Main;
