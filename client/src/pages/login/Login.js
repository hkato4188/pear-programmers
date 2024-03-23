import React, { useState, useContext } from "react";
import { useHistory } from "react-router-dom";
import { UserContext } from "../../context/user";

function Login() {
  const { user, updateUser } = useContext(UserContext);
  const [signUp, setSignUp] = useState(false);
  const [errors, setErrors] = useState(null);
  const history = useHistory();

  const initialState = {
    name: "",
    email: "",
    password: "",
  };

  const [formState, setFormState] = useState(initialState);
  const changeFormState = (event) => {
    const { name, value } = event.target;
    setFormState({ ...formState, [name]: value });
  };

  const handleClick = () => setSignUp((signUp) => !signUp);

  const postToLoginOrSignup = (event) => {
    event.preventDefault();

    const postRequest = {
      method: "POST",
      headers: {
        "content-type": "application/json",
        accept: "application/json",
      },
      body: JSON.stringify(formState),
    };
    console.log("signUp value is: ");
    console.log(signUp);
    fetch(signUp ? "/signup" : "/login", postRequest)
      .then((r) => r.json())
      .then((userData) => {
        if (userData.errors) {
          setErrors(userData.errors);
        } else {
          setErrors(null);
          updateUser(userData);
          history.push("/");
        }
      })
      .catch((err) => {
        console.log("error", err);
      });
  };

  return (
    <div className="login-container">
      <div className="login-signup-box">
        <h1>{signUp ? "Already a member?" : "Not a member?"}</h1>

        <button onClick={handleClick}>
          {signUp ? "Log In!" : "Register now!"}
        </button>
      </div>

      <div className="box-border">
        <h1 style={{ color: "red" }}>
          {" "}
          {errors ? errors.map((error) => <h5>{error}</h5>) : null}
        </h1>

        <h1>Enter your username | email to log in:</h1>
        <form className="login-form" onSubmit={postToLoginOrSignup}>
          <label>Username</label>
          <input
            type="text"
            name="name"
            placeholder="Enter email or Username"
            value={formState.name}
            onChange={changeFormState}
          />
          <>
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter email or Username"
              value={formState.email}
              onChange={changeFormState}
            />
          </>
          <>
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter password"
              value={formState.password}
              onChange={changeFormState}
            />
          </>
          <input
            className="input-button"
            type="submit"
            value={signUp ? "Sign Up!" : "Log In!"}
          />
        </form>
      </div>
    </div>
  );
}

export default Login;
