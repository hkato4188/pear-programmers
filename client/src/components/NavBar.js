import React, { useContext } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../context/user";

function NavBar() {
  const { user, updateUser } = useContext(UserContext);

  function handleLogout() {
    updateUser(null);
    fetch("/logout", { method: "DELETE" });
  }

  return (
    <div>
      {user ? (
        <NavLink exact to="/">
          About
        </NavLink>
      ) : null}
      {!user ? (
        <NavLink exact to="/login">
          Login Signup
        </NavLink>
      ) : null}
      {user ? (
        <a href="/logout" onClick={handleLogout}>
          Logout
        </a>
      ) : null}
    </div>
  );
}

export default NavBar;
