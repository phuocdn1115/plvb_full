import React from 'react';



function HomePage() {
    return (
        <div className="mb-3">
            <nav className='navbar navbar-dark bg-primary'>
                <div className='container-fluid'>
                    <a className='navbar-brand' href="#">
                        PLVB App
                    </a>
                </div>
            </nav>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-2">
                        <div class="card h-100">
                            <div class="card-body">
                                <h5 class="card-title">Welcome {localStorage.getItem('username')}</h5>
                                <ul class="list-group">
                                    <li class="list-group-item"><a href="#">User</a></li>
                                    <li class="list-group-item"><a href="#">File</a></li>
                                    <li class="list-group-item"><a href="#">Services</a></li>
                                    <li class="list-group-item"><a href="/login">Logout</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-9">
                        <h1>Main Content</h1>
                        <p>This is the main content of your page.</p>
                    </div>
                </div>
            </div>
        </div>

    )
}

export default HomePage