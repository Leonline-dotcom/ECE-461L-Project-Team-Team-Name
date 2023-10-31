
import './App.css';
import React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import {TextField} from '@mui/material';
import { Grid } from '@mui/material';
 
function AppPage() {

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
      
      <div>
         <br/>
         <br/>
         <Box  bgcolor="primary.main" sx={{ border: '1px dashed grey' } }>
 
        {this.props.name}
          
        </Box>
        <br/>
        <br/>
        <Grid container spacing={2}>
        <Grid xs={8}>
        <Box  sx={{ border: '1px dashed grey',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-evenly' } }>
        <HardwareSet capacity = "200"/>
        <HardwareSet capacity = "200"/>
        </Box>
        </Grid>
        <Grid xs={4}>
        <Box sx={{ border: '1px dashed grey' } }>
        Member 1 <br/>
        Member 2 <br/>
        Member 3 <br/>
        <Button variant="contained" onClick={this.handleClick}>Join</Button>
        </Box>
        </Grid>
        </Grid>
      </div>
     )
    }
  }

  return (
    <div className="AppPage">
      
      <h1 className={AppPage.header}> Project Page</h1>
      
      <Project name = "Project 1"/>
      <br/>
      <Project name = "Project 2"/>
      <br/>
      <Project name = "Project 3"/>
      <br/>
      <Project name = "Project 4"/>
      <br/>

    </div>
  );
}

export default AppPage;
