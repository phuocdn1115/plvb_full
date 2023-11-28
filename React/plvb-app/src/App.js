import React, { useState, useEffect } from "react"
import api from './api'
import { toast } from 'react-toastify';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './Login'
import HomePage from "./Home";

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    label: '',
    desc: ''
  });

  const fetchLabel = async () => {
    const response = await api.get('/get_label/');
    setTransactions(response.data)
  };

  useEffect(() => {
    // fetchLabel();
  }, []);

  const handleInputChange = (event) => {
    setFormData({
      ...formData
    });
  };



  const handleFormSubmit = async (event) => {
    event.preventDefault();
    const res = await api.post('/auth/token', formData);
    setFormData({
      username: '',
      password: ''
    });
    if (res) {
      toast('Login success', res.username)
    }
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/login' element={<Login />}></Route>
        <Route path='/homepage' element={<HomePage />}></Route>
      </Routes>
    </BrowserRouter>
  )

}

export default App;
