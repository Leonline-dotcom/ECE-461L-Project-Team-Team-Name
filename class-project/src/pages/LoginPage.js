import {useState} from "react"
import {Link, Route, Routes } from "react-router-dom";
import{ Box, Button, TextField, Typography} from "@mui/material"
import "../form.css"


function LoginPage(){
    const AdminUser ={
        username: "admin",
        password: "123"
    }
    const [User, setUsername] = useState({username :""});
    const [Pass, setPassword] = useState({pass :""});
    const [Error, ]=useState("");
    function setUser(val){
        setUsername({ username: val.target.value })
        console.log(User.username)
    }
    function setPass(val){
        setUsername({ pass: val.target.value })
        console.log(Pass.pass)
    }
// TODO: Edit to accompany backend
    function ButtonClick({type}) {
        if (type== "Login"){
            if(User.username == "admin" && Pass.pass =="123"){

            }
        }else{
            if(User.username == "admin" && Pass.pass =="123"){

            }
        }
         
    }
    

    return(
        <>
       <form>
            <Box 
            display="flex"
            flexDirection={"column"} 
            maxWidth={400} 
            alignItems="center" 
            justifyContent={"center"}
            margin="auto"
            marginTop={5}
            padding={5}
            borderRadius={5}
            boxShadow={"5px 5px 10px #ccc"}>
                <Typography variant="h2" padding={3}> Login</Typography>
                <TextField
                margin="normal"
                    required
                    id="outlined-required"
                    label="Username"
                    onChange={e => setPassword}
                />
                <TextField
                margin="normal"
                    required id="outlined-required"
                    label="Password"
                    type="password"
                    onChange={e => setUsername}
                />
                <div className="buttons">
                <Button variant="contained" onClick={ButtonClick({type:"Login"})}>Log In</Button>
                <Link><Button variant="contained" onClick={ButtonClick({type:"Signup"})}>Signup</Button></Link>
                </div>
                
            </Box>
        </form> </>
    )
}

export default LoginPage