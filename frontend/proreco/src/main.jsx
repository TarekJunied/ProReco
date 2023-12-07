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
import AboutPage from './pages/AboutPage.jsx'
import ErrorBoundary from './components/ErrorBoundary.jsx'
import ContactPage from './pages/ContactPage.jsx';
const router = createBrowserRouter([
  {
    path: '', // Empty path for the default route
    element: <ErrorBoundary><LandingPage /></ErrorBoundary>,
  },
  {
    path: "/",
    element: <ErrorBoundary><LandingPage /></ErrorBoundary>,
  },
  {
    path: "/start",
    element: <ErrorBoundary><StartPage /></ErrorBoundary>,
  },
  {
    path: "/loading",
    element: <ErrorBoundary><LoadingPage /></ErrorBoundary>,
  },
  {
    path: "/ranking",
    element: <ErrorBoundary><RankingPage /></ErrorBoundary>,
  },
  {
    path: "/recommend",
    element: <ErrorBoundary><RecommendPage /></ErrorBoundary>,
  },
  {
    path: "/about",
    element: <ErrorBoundary><AboutPage /></ErrorBoundary>,
  },
  {
    path: "/contact",
    element: <ErrorBoundary><ContactPage /></ErrorBoundary>,
  },
  {
    // Add a wildcard route to catch all unknown paths
    // TODO: add a NotFound Page
    path: "*",
    element: <ErrorBoundary><LandingPage /></ErrorBoundary>,
  }
]);


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />

  </React.StrictMode>,
)

