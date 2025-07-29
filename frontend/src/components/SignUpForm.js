// SignupForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

const SignupForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await axios.post('http://127.0.0.1:8000/shecodes/signup', formData);
    setMessage(response.data.message || 'Signup successful');
  } catch (error) {
    console.error('Error:', error); // Log the full error
    setMessage(error.message); // Shows "Network Error" by default 
  }
};


  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" placeholder="Username" onChange={handleChange} value={formData.username} /><br/>
        <input name="password" type="password" placeholder="Password" onChange={handleChange} value={formData.password} /><br/>
        <button type="submit">Sign Up</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default SignupForm;
