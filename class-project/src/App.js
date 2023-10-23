import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import SignUpPage from './SignUpPage';
import AppPage from './ApplicationPage';
function App() {
  return (
    <Router>
      <Route>
        <Route path="/login" component={LoginPage} />
        <Route path="/signup" component={SignUpPage} />
        <Route path="/appPage" component={AppPage} />
      </Route>
    </Router>
  );
}

export default App;
