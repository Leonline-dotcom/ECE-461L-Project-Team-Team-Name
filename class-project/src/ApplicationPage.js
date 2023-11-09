
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
  const [HWSet1Cap, setHWSet1Cap] = useState(0);
  const [HWSet2Cap, setHWSet2Cap] = useState(0);
  class HardwareSet extends React.Component{


    constructor(props){
      super(props)
      this.handleClick=this.handleClick.bind(this)
      this.minusClick=this.minusClick.bind(this)
      this.handleamountChange=this.handleamountChange.bind(this)
      this.getHardware()
      this.state={
       checkedOut:0,
        amount:0, 
    }
    
  }
  getHardware(){
    const self = this;
    fetch("appPage/getHardware/"+this.props.name+"/"+this.props.HWSetname)
    
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .then(function(data){
      
     data=JSON.parse(data);
      
    
  
      if(data.code===200)
      {
        console.log(data)
        self.setState({checkedOut:data.qty})
        
      }
    }
    )
      
    }
  
  handleamountChange= (e) => this.setState({ 
		amount: e.target.value 
	}) 
 
    handleClick(){
      const self = this;
    fetch("appPage/checkOut/"+this.props.name+"/"+this.state.amount+"/"+this.props.HWSetname)
    
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .then(function(data){
      
     data=JSON.parse(data);
      
    
  
      if(data.code===200)
      {
        console.log(data)
        self.setState({checkedOut:data.qty})
        setTimeout(() => {
          navigate('/appPage',{ state: { data: Username } });;
        }, 500);
      }
    }
    )
      
    }
    minusClick(){
      const self = this;
    fetch("appPage/checkIn/"+this.props.name+"/"+this.state.amount+"/"+this.props.HWSetname)
    
    .then((response) => response.text())
    //.then((data) => console.log(data))
    .then(function(data){
      
     data=JSON.parse(data);
      
    
  
      if(data.code===200)
      {
        console.log(data)
        self.setState({checkedOut:data.qty})
        setTimeout(() => {
          navigate('/appPage',{ state: { data: Username } });;
        }, 500);
      }
    }
    )
      }
    
    render(){
      console.log(this.state.amount )
      
      return(
        <div>
          
          
          
         
          
         
          
          <center>
          {this.props.HWSetname}
          <br/>
          Global Capacity: {this.props.capacity} <br/>
          CheckedOut: {this.state.checkedOut}<br/>
          <TextField id="standard-basic" label="Amount" variant="standard"  onChange={this.handleamountChange}  input type="number"/><br/><br/>
          <Box  >
        
      <Button variant="contained" onClick={this.handleClick}>+</Button>
      <Button variant="contained" onClick={this.minusClick}>-</Button>
    </Box>
    <br/>
        
    </center>
    
        </div>
        
      )
    }
    
  }

  class Project extends React.Component{
    
    constructor(props){
      super(props)
      this.LeavehandleClick=this.LeavehandleClick.bind(this)
      
    }
    
    
    LeavehandleClick(){
      fetch('appPage/leaveProject/'+this.props.name+"/" + Username)
    .then((response) => response.text())
    .then(function(data) {
      data = JSON.parse(data);
    
      if (data.code === 200) {
        setTimeout(() => {
          navigate('/appPage',{ state: { data: Username } });;
        }, 500);
        
      } 
    });
  
    
  }
    render(){
     return(
      
      <div className="App">
         <br/>
         <br/>
         <Box  bgcolor="primary.main" sx={{ border: '1px dashed grey' } }>
 
        {this.props.name}
          
        
        

         
        </Box>
        <br/>
        <br/>
        <Grid container spacing={2}>
        <Grid xs={12}>
        <Box sx={{ border: '1px dashed grey' } }>
        <HardwareSet capacity = {HWSet1Cap} HWSetname='HWSet1' name={this.props.name}/>
        <HardwareSet capacity = {HWSet2Cap} HWSetname='HWSet2'name={this.props.name}/>

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
      this.addExistingItem=this.addExistingItem.bind(this)
      this.getProjectList()
      this.gobalCapacity()
      this.state = {
        userInput:"",
        list:[],
      }
      
    }
    gobalCapacity(){
      fetch('appPage/getcapacity')
    .then((response) => response.text())
    .then(function(data) {
      data = JSON.parse(data);
      setHWSet1Cap(data.HWSet1)
      setHWSet2Cap(data.HWSet2)
    })
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
            setErrorMess("")
            setError(false)
              fetch('appPage/addProjectToUser/' + stateString + '/' + Username)
              .then((response) => response.text())
        .then(function(data) {})
        setTimeout(() => {
          navigate('/appPage',{ state: { data: Username } });;
        }, 500);

          } else {
            setError(true);
            setErrorMess(data.message);
          }
          
        });
    }
  }
  addExistingItem() {
    const stateString = JSON.stringify(this.state.userInput);
    fetch('appPage/searchProject/' + stateString)
      .then((response) => response.text())
      .then(function (data) {
        data = JSON.parse(data);
  
        if (data.code === 200) {
          setErrorMess("")
          setError(false)
          fetch('appPage/addProjectToUser/' + stateString + '/' + Username)
              .then((response) => response.text())
        .then(function(data) {}) 
        
        setTimeout(() => {
          navigate('/appPage',{ state: { data: Username } });;
        }, 500);
        
        } else {
          setError(true);
            setErrorMess(data.message);
        }
        

  }); 
 
    ;
}
  getProjectList(){
    const self = this; // Store a reference to 'this'
    console.log('im talking to you');
    fetch('appPage/getprojects/' + Username)
    .then((response) => response.text())
    .then(function(data) {
      data = JSON.parse(data);

      if (data.code === 200) {
          self.setState((prevState) => ({
            list: [...prevState.list, data.projectlist],
            userInput: "",
          }));
        
      } 
    });

    
  }
 
    render(){
      console.log(this.state.list)
      
      return(
       
       <div>
       <Grid className="list-group">
  {this.state.list.map((item, index) => {
    console.log(item);
    return item.map((nestedItem, nestedIndex) => (
      <Box className="list-group-item" key={nestedIndex}>
        {console.log(nestedItem)}
        <Project name={nestedItem} />
      </Box>
      
    ));
    
  })}
</Grid>
<br/>
        
        <br/>
<Grid className="errorcolor"><center>{errorMess}</center></Grid>


        <br/>
        
        <br/>

    <Grid container spacing={2}>
        <Grid xs={6}>
        <Box  sx={{ border: '1px dashed grey',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-evenly' } }>
        <HardwareSet capacity = "200"/>
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
        <Button variant="contained" onClick={this.addExistingItem}>Submit</Button> <br/>
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
      
      

  
        
        <JoinProjects/>

        
        
        
        
    </div>
  );
}

export default AppPage;
