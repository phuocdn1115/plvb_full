import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Validation from './LoginValidation';
import api from './api'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


function Login() {
    const navigate = useNavigate()
    const [errors, setErrors] = useState([])
    const [values, setValues] = useState({
        username: '',
        password: ''
    })

    const handleFormSubmit = (async event => {
        console.log('handleFormSubmit')
        event.preventDefault();
        setErrors(Validation(values))
        console.log(errors.username)
        if (errors.username === undefined && errors.password === undefined){
             const payload = new FormData()

        payload.append("username", values.username)
        payload.append("password", values.password)
        const res = await api.post('/auth/token', payload, {
            headers: { "Content-Type": "multipart/form-data" },
        })
        if (res.data.id) {
            localStorage.setItem("username", res.data.username)
            navigate('/homepage')
        }
        else {
            
        }
        }
    })

    const handleInputChange = (event => {
        setValues(prev => ({ ...prev, [event.target.name]: [event.target.value] }))
    })

    return (
        <div className="mb-3">
            <nav className='navbar navbar-dark bg-primary'>
                <div className='container-fluid'>
                    <a className='navbar-brand' href="#">
                        PLVB App
                    </a>
                </div>
            </nav>
            <form action='' onSubmit={handleFormSubmit}>
                <p className="text-start">Đăng nhập</p>
                <div className="mb-2 row">
                    <label htmlFor="text" className="col-sm-1 ">Username</label>
                    <div className="col-sm-2">
                        <input type="text" className="form-control" onChange={handleInputChange} placeholder="Username" id="inputUsername" name='username'></input>
                        {errors.usename && <span className='text-danger'>{errors.username}</span>}
                    </div>
                </div>
                <div className="mb-2 row">
                    <label htmlFor="text" className="col-sm-1 ">Password</label>
                    <div className="col-sm-2">
                        <input type="password" className="form-control" onChange={handleInputChange} id="inputPassword" name='password'></input>
                        {errors.password && <span className='text-danger'>{errors.password}</span>}
                    </div>
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>

        </div>
    )
}

export default Login