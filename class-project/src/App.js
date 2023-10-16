import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import SignUpPage from './SignUpPage';

function App() {
  return (
    <Router>
      <Route>
        <Route path="/login" component={LoginPage} />
        <Route path="/signup" component={SignUpPage} />
      </Route>
    </Router>
  );
}

export default App;
