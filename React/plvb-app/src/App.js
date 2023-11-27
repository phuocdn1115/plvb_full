import React, { useState, useEffect } from "react"
import api from './api'

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
    await api.post('/label/', formData);
    fetchLabel();
    setFormData({
      lable: '',
      desc: ''
    });
  };

  return (
    <div>
      <nav className='navbar navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href="#">
            PLVB App
          </a>
        </div>
      </nav>
      <form>
        <p class="text-start">Đăng nhập</p>
        <div class="mb-2 row">
          <label for="inputText" class="col-sm-1   col-form-label border">Username</label>
          <div class="col-sm-2">
            <input type="text" class="form-control" placeholder="Username" id="inputUsername" ></input>
          </div>
        </div>
        <div class="mb-2 row">
          <label for="inputPassword" class="col-sm-1 col-form-label border">Password</label>
          <div class="col-sm-2">
            <input type="password" class="form-control" id="inputPassword"></input>
          </div>
        </div>
      </form>
      <div >

      </div>

      {/* <table class="table table-striped">
        <thead>
          <tr>
            <td>Label</td>
            <td>Desc</td>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.label}</td>
              <td>{transaction.desc}</td>
            </tr>
          ))}
        </tbody>
      </table> */}
    </div>
  )

}

export default App;

