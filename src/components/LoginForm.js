import React, { useState } from "react";
import axios from "axios";

const LoginForm = () => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/shecodes/login", {
        username:userId,
        password:password
      });

      setMessage("Login successful!");
      console.log(response.data);
    } catch (error) {
      setMessage("Invalid credentials");
      console.error("Login failed:", error.response?.data || error.message);
    }
  };

  return (
    <div style={{ margin: "2rem" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>User ID:</label><br />
          <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} required />
        </div>
        <div>
          <label>Password:</label><br />
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit" style={{ marginTop: "10px" }}>Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};


export default LoginForm;
