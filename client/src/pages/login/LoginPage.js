import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import { UserContext } from "../../context/user";
import Login from "./Login";
import About from "../about/About";

function LoginPage() {
  return (
    <div>
      <Login />
    </div>
  );
}

export default LoginPage;
