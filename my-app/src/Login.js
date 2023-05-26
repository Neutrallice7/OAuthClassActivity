import React, { useState } from "react";
import axios from "axios";
import bcrypt from "bcryptjs";
const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault(); //Disable the default submission behavior
    try {
      const hashedPassword = await bcrypt.hash(password, 10);
      const response = await axios.post("http://localhost:8000/token", {
        username: username,
        password: hashedPassword,
      });
      const { access_token } = response.data;
      console.log("Login successful");
    } catch (error) {
      console.log("Login failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label>
          Username
          <input
            type='text'
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </label>
        <br />
        <label>
          Password
          <input
            type='password'
            value={password}
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
