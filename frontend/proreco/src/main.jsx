import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import LandingLayout from "./layout/LandingLayout.jsx"
import StartPage from './pages/StartPage.jsx';
import LoadingPage from './pages/LoadingPage.jsx';
import RankingPage from './pages/RankingPage.jsx';
import RecommendPage from "./pages/RecommendPage.jsx";
import LandingPage from './pages/LandingPage.jsx';
import AboutPage from './pages/AboutPage.jsx'
import ErrorBoundary from './components/ErrorBoundary.jsx'
import ContactPage from './pages/ContactPage.jsx';
import PetriNetPageTest from './pages/PetriNetPageTest';
import MinePage from './pages/MinePage.jsx';
import PetriNetView from "./pages/PetriNetView.jsx"
import GenerateLogPage from './pages/GenerateLogPage.jsx';
import AfterGeneration from './pages/AfterGeneration.jsx';
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
    path: "/test",
    element: <LandingLayout />
  },
  {
    path: "/generateLog",
    element: <ErrorBoundary><GenerateLogPage /></ErrorBoundary>
  },
  {
    path: "/afterGeneration",
    element: <ErrorBoundary><AfterGeneration /></ErrorBoundary>
  },
  {
    path: "/mine",
    element: <ErrorBoundary><MinePage /></ErrorBoundary>
  },
  {
    path: "/viewPetriNet",
    element: <ErrorBoundary><PetriNetView /></ErrorBoundary>
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

