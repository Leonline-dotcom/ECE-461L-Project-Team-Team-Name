import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import SignUp from './SignUpPage'
import Login from './LoginPage'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

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
    <SignUp/>
  </React.StrictMode>
);