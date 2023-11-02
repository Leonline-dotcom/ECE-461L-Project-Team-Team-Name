
import './App.css';
import React, {useState} from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import {TextField} from '@mui/material';
import { Grid } from '@mui/material';
import styles from './StyleSheet.module.css';
import { useLocation } from 'react-router-dom'; 
import { useNavigate } from 'react-router-dom';

function AppPage() {
  const location = useLocation();
  const Username = location.state.data;
  const navigate = useNavigate();
  const [error, setError] = useState(false);
  const [errorMess, setErrorMess] = useState("");
  class HardwareSet extends React.Component{


    constructor(props){
      super(props)
      this.handleClick=this.handleClick.bind(this)
      this.minusClick=this.minusClick.bind(this)
      this.handleamountChange=this.handleamountChange.bind(this)
      
      this.state={
       checkedOut:0,
        amount:0, 
    }
    
  }
  handleamountChange= (e) => this.setState({ 
		amount: e.target.value 
	}) 
  
    handleClick(){
      if(parseInt(this.state.checkedOut) + parseInt(this.state.amount)<this.props.capacity){
      var newCheckedOut = parseInt(this.state.checkedOut) + parseInt(this.state.amount)
      this.setState({checkedOut: newCheckedOut})
      }
      else{
        this.setState({checkedOut: this.props.capacity})
      }
    }
    minusClick(){
      if(parseInt(this.state.checkedOut) - parseInt(this.state.amount)>0){
        var newCheckedOut = parseInt(this.state.checkedOut) - parseInt(this.state.amount)
        this.setState({checkedOut: newCheckedOut})
        }
        else{
          this.setState({checkedOut: 0})
        }
      }
    
    render(){
      console.log(this.state.amount )
      return(
        <div>
          
          
          
         
          
         
          
          <center>
          {this.props.name}
          <br/>
          Capacity: {this.props.capacity} <br/>
          CheckedOut: {this.state.checkedOut} / {this.props.capacity}<br/>
          <TextField id="standard-basic" label="Amount" variant="standard"  onChange={this.handleamountChange}  input type="number"/><br/><br/>
          <Box  >
        
      <Button variant="contained" onClick={this.handleClick}>+</Button>
      <Button variant="contained" onClick={this.minusClick}>-</Button>
    </Box>
    </center>
        </div>
      )
    }
    
  }

  class Project extends React.Component{
    
    constructor(props){
      super(props)

    }

    render(){
     return(
      
      <div className="App">
         <br/>
         <br/>
         <Box  bgcolor="primary.main" sx={{ border: '1px dashed grey' } }>
        <center>{this.props.name}</center>
        
          
        
        

         
        </Box>
        <br/>
        <br/>
        <Grid container spacing={2}>
        <Grid xs={12}>
        <Box sx={{ border: '1px dashed grey' } }>
        <HardwareSet capacity = "200" name='HwSet1'/>
        <HardwareSet capacity = "200" name='HwSet2'/>
        <br/>
        <Button variant="contained" onClick={this.handleClick}>Leave</Button>
        <br/>
        <p></p>
        </Box>
        </Grid>
        
        </Grid>
      </div>
     )
    }
  }
  class JoinProjects extends React.Component{
    constructor(props){
      super(props)
      this.handleInputChange=this.handleInputChange.bind(this)
      this.addItem=this.addItem.bind(this)
      this.state = {
        userInput:"",
        list:[],
      }
      
    }

    handleInputChange= (e) => this.setState({ 
      userInput: e.target.value 
    }) 
    addItem() {
      if (this.state.userInput !== "") {
      const stateString = JSON.stringify(this.state.userInput);
      const self = this; // Store a reference to 'this'
      
      console.log(this.state.userInput);
      
      fetch('appPage/addProject/' + stateString)
        .then((response) => response.text())
        .then(function(data) {
          data = JSON.parse(data);
    
          if (data.code === 200) {
            
              const newItem = {
                name: self.state.userInput,
              };
              self.setState((prevState) => ({
                list: [...prevState.list, newItem], // Use prevState to update the list
                userInput: "",
              }));
              fetch('appPage/addProjectToUser/' + stateString + '/' + Username)
              .then((response) => response.text())
        .then(function(data) {})
            
          } else {
            setError(true);
            setErrorMess(data.message);
          }
        });
    }
  }
    
    render(){
      console.log(this.state.list)
      return(
       
       <div>
       <Grid className="list-group">
          {this.state.list.map((item, index) => (
            
            <Box className="list-group-item" key={index}>
               {item.index}
               {console.log(item.index)}
              <Project name={item.name} />
            </Box>
          ))}
        </Grid>
        <br/>
        <br/>
    <Grid container spacing={2}>
        <Grid xs={6}>
        <Box sx={{ border: '1px dashed grey' } }>
        <center>
        Create New Project
        <br/>
        <TextField id="standard-basic" label="Project Name" variant="standard" onChange={this.handleInputChange} /><br/><br/>
        <Box><Button variant="contained" onClick={this.addItem}>Submit</Button> <br/></Box>
        
        <p></p>
        </center>
      

        </Box>
        </Grid>
        
        <Grid xs={6}>
        <Box sx={{ border: '1px dashed grey' } }>
        <center>
        Join Existing Project
        <br/>
        <TextField id="standard-basic" label="Project Name" variant="standard" onChange={this.handleInputChange} /><br/><br/>
        <Button variant="contained" onClick={this.addItem}>Submit</Button> <br/>
        <p></p>
        </center>
      

        </Box>
        </Grid>
        
        </Grid>
       </div>
      )
    }
  }
  class LogOutButton extends React.Component{
    constructor(props){
      super(props)
      this.handleLogOut=this.handleLogOut.bind(this)
    }
    handleLogOut(){
      navigate('/login')
    }
    render(){
      return(
        <div><Button variant="contained" onClick={this.handleLogOut}>Log Out</Button> <br/></div>
        
      )
    }
  }
  return (
    <div className="AppPage">
     
      <center>
      <h2>{Username}</h2>
      <LogOutButton/>
        <h1 className={styles.header}> Project Page</h1>
        
        </center>
      
      
      {/* <Project name = "Project 1"/>
      <br/>
      <Project name = "Project 2"/>
      <br/>
      <Project name = "Project 3"/>
      <br/>
      <Project name = "Project 4"/>
      <br/> */}
  
        
        <JoinProjects/>

        
        
        
        
    </div>
  );
}

export default AppPage;
