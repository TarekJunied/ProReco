import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import StartPage from './pages/StartPage.jsx';
import LoadingPage from './pages/LoadingPage.jsx';
import RankingPage from './pages/RankingPage.jsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/start",
    element: <StartPage />,
  },
  {
    path: "/loading",
    element: <LoadingPage />,
  },
  {
    path: "/ranking",
    element: <RankingPage />,
  },
]);


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
