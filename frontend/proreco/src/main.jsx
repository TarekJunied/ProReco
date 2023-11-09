import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import StartPage from './pages/StartPage.jsx';
import LoadingPage from './pages/LoadingPage.jsx';
import RankingPage from './pages/RankingPage.jsx';
import RecommendPage from "./pages/RecommendPage.jsx";
import LandingPage from './pages/LandingPage.jsx';
const router = createBrowserRouter([
  {
    path: '', // Empty path for the default route
    element: <LandingPage />,
  },
  {
    path: "/",
    element: <LandingPage />,
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
  {
    path: "/recommend",
    element: <RecommendPage />,
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />

  </React.StrictMode>,
)

