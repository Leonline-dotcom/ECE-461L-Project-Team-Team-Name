import React,  { useState } from "react";
import ReactDOM from 'react-dom/client';
import AppPage from './ApplicationPage';
import styles from './StyleSheet.module.css'
import { useNavigate } from 'react-router-dom';
const SignUp= () => {
  const [User, setUsername] = useState("");
  const [Pass, setPassword]=useState("");
  const [error, setError] = useState(false);
  const [errorMess, setErrorMess] = useState("");
  const navigate = useNavigate();
  function getUser(val){
    setUsername(val.target.value)
  }
  function getPass(val){
    setPassword(val.target.value)
  }
  const clickHandler = () => {
    
    fetch("signup/"+User+"/"+Pass)
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .then(function(data){
      
     data=JSON.parse(data);
      
      
  
      if(data.code===200)
      {
        console.log("hi")
        
        
        navigate('/appPage',{ state: { data: User } });
      }
      else{
        setError(true)
        setErrorMess(data.error)
      }
      })
      
    
    
    }

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
            
            <h3>Sign-Up</h3>
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
            <button onClick={clickHandler}>Sign Up</button>
            <div className="back-to-login-container">
        Already have an account? <a href="/login">Login</a>
      </div>
        </center>
    </div>
    );
    }

export default SignUp;
    