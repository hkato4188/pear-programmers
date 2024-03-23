import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../../context/user";

function NavBar() {
  const { user, updateUser } = useContext(UserContext);

  function handleLogout() {
    updateUser(null);
    fetch("/logout", { method: "DELETE" });
  }

  return (
    <div className="nav-container">
      {user ? (
        <NavLink className="nav-text btn" exact to="/">
          About
        </NavLink>
      ) : null}
      {user ? (
        <NavLink className="nav-text btn" exact to="/todolists">
          ToDo Lists
        </NavLink>
      ) : null}
      {!user ? (
        <NavLink className="nav-text btn" exact to="/login">
          Login|Signup
        </NavLink>
      ) : null}
      {user ? (
        <a className="nav-text btn" href="/logout" onClick={handleLogout}>
          Logout
        </a>
      ) : null}
    </div>
  );
}

export default NavBar;
