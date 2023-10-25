import React,  { useState } from "react";
import ReactDOM from 'react-dom/client';
import AppPage from './ApplicationPage';
const SignUp= () => {
  const [User, setUsername] = useState("");
  const [Pass, setPassword]=useState("");
  const [error, setError] = useState(false);
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
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(
          <React.StrictMode>
            <AppPage />
          </React.StrictMode>
        )
      }
      else{
        setError(true)
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
        <p >Error: Username Is Already In Use. Please Try Again</p>
      </div>
      );
    };

    return (
    <div>
        
        <center>
            
            <h3>Sign-Up</h3>
            <div className="messages">
		        {errorMessage()}
	          </div>
            <h3>{User}</h3>
            <h3>Username</h3>
            <input
              type="text"
              placeholder="Enter the Username..."
              onChange={getUser}
            ></input>
            <h3>{Pass}</h3>
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
    