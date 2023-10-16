import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import SignUp from './SignUpPage'
import Login from './LoginPage'
import AppPage from './ApplicationPage';
import {
  createBrowserRouter,
  RouterProvider,
  BrowserRouter
} from "react-router-dom";


const router = createBrowserRouter([
  {
    path: "/",
    children:[
      {
        path: "",
        element: <Login/>
      },
      {
        path:"appPage",
        element: <AppPage/>
      },
      {
        path: "login",
        element: <Login/>,
      },
      {
        path: "/signup",
        element: <SignUp/>,
      },
    ]
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
{/* 
    <BrowserRouter>
    <SignUp />
    </BrowserRouter> 
    
Stashed changes */}
  </React.StrictMode>
);