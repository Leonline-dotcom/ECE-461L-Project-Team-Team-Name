import React,  { useState } from "react";
import ReactDOM from 'react-dom/client';
import AppPage from './ApplicationPage';

import styles from './StyleSheet.module.css'
const Login= () => {
  const [User, setUsername] = useState("");
  const [Pass, setPassword]=useState("");
  const [error, setError] = useState(false);
  const [errorMess, setErrorMess] = useState("");
  function getUser(val){
    setUsername(val.target.value)
  }
  function getPass(val){
    setPassword(val.target.value)
  }
    const clickHandler = () => {

      fetch("login/"+User+"/"+Pass)
      .then((response) => response.text())
      //.then((data) => console.log(data))
      .then(function(data){
        
       data=JSON.parse(data);
        
        
    
        if(data.code===200)
        {
          const root = ReactDOM.createRoot(document.getElementById('root'));
          root.render(
            <React.StrictMode>
              <AppPage />
            </React.StrictMode>
          )
        }
        else{
          setError(true)
          setErrorMess(data.error)
        }
        })
        
      
      
      
  
    };

    const errorMessage = () => {
      return (
      <div
        className="error"
        style={{
        display: error ? '' : 'none',
        }}>
        <p >{errorMess}</p>
      </div>
      );
    };



    return (
    <div>
        <center>  
            <h3>Login</h3>
            <div className={styles.errorcolor}>
		        {errorMessage()}
	          </div>
            
            <h3>Username</h3>
            <input
              type="text"
              placeholder="Enter the Username..."
              onChange={getUser}
            ></input>
            
            <h3>Password</h3>
            <input
              type="text"
              placeholder="Enter the Password..."
              onChange={getPass}
            ></input>
            <br></br>
            <button onClick={clickHandler}>Login</button>
            <div className="back-to-login-container">
        Don't have an account? <a href="signup">SignUp</a>
      </div>
            
        </center>
    </div>
    );
    }

export default Login;
    