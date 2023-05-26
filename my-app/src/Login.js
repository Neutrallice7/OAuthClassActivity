import React, { useState } from "react";

const Login = () => {
  const [email, setUsername] = useState("");
  const [hashed_password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault(); // Disable the default submission behavior

    try {
      const response = await fetch("http://localhost:8000/api/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          hashed_password: hashed_password,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const { access_token } = data;
        console.log("Login successful");
      } else {
        console.log("Login failed");
      }
    } catch (error) {
      console.log("Login failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>
          eMAIL
          <input
            type='text'
            value={email}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password
          <input
            type='hashed_password'
            value={hashed_password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <br />
        <button type='submit'>Login</button>
      </form>
    </div>
  );
};

export default Login;
