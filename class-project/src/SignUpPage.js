import React,  { useState } from "react";
const clickHandler = () => {
};
const SignUp= () => {
    return (
    <div>
        <center>
            <h3>Sign-Up</h3>
            <h3>Username</h3>
            <input
              type="text"
              placeholder="Enter the Username..."
            ></input>
            <h3>Password</h3>
            <input
              type="text"
              placeholder="Enter the Password..."
              
            ></input>
            <br></br>
            <button onClick={clickHandler}>Sign Up</button>
        </center>
    </div>
    );
    }

export default SignUp;
    