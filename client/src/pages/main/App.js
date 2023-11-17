import React from "react";
import Authenticate from "../login/Authenticate";
import { UserProvider } from "../../context/user";
import Header from "./Header";
function App() {
  return (
    <UserProvider>
      <div className="page-border">
        <Header />
        <Authenticate />
      </div>
    </UserProvider>
  );
}

export default App;
