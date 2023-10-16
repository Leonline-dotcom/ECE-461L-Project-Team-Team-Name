import React,  { useState } from "react";

const Login= () => {
  const [User, setUsername] = useState("");
  const [Pass, setPassword]=useState("");
  function getUser(val){
    setUsername(val.target.value)
  }
  function getPass(val){
    setPassword(val.target.value)
  }
    const clickHandler = () => {
    };
    return (
    <div>
        <center>  
            <h3>Login</h3>
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
            <button onClick={clickHandler}>Loginp</button>
            <div className="back-to-login-container">
        Don't have an account? <a href="/signup">SignUp</a>
      </div>
            
        </center>
    </div>
    );
    }

export default Login;
    