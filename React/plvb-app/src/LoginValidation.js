function Validation(values){
    let error={}

    if (values.username ===''){
        error.username = 'Username is wrong'
    } else error.username = ''
    if (values.password ===''){
        error.password = 'Password is wrong'
    } else error.password = ''

    return error;
}

export default Validation;