import React from "react";
import Authenticate from "./pages/login/Authenticate";
import Header from "./pages/main/Header";
import { UserProvider } from "./context/user";

function App() {
  return (
    <UserProvider>
      <div>
        <Header />
        <Authenticate />
      </div>
    </UserProvider>
  );
}

export default App;
