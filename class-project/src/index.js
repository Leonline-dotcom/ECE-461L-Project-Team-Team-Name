import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
<<<<<<< Updated upstream
import SignUp from './SignUpPage'
import Login from './LoginPage'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
=======
import LoginPage from './pages/LoginPage';
import {BrowserRouter} from "react-router-dom"
import reportWebVitals from './reportWebVitals';
import SignUp from './pages/SignUpPage';
>>>>>>> Stashed changes

const router = createBrowserRouter([
  {
    path: "/",
    children:[
      {
        path: "login",
        element: <Login/>,
      },
      {
        path: "signup",
        element: <SignUp/>,
      },
    ]
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
<<<<<<< Updated upstream
    <RouterProvider router={router} />
=======
    <BrowserRouter>
    <SignUp />
    </BrowserRouter> 
>>>>>>> Stashed changes
  </React.StrictMode>
);