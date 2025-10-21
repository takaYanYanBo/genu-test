import './i18n/config';
import React from 'react';
import ReactDOM from 'react-dom/client';
import AuthWithUserpool from './components/AuthWithUserpool';
import AuthWithSAML from './components/AuthWithSAML';
import './index.css';
import {
  RouterProvider,
  createBrowserRouter,
  RouteObject,
} from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Setting from './pages/Setting';
import SharedChatPage from './pages/SharedChatPage';
import NotFound from './pages/NotFound';
import AgentCorePage from './pages/AgentCorePage.tsx';
import { Authenticator } from '@aws-amplify/ui-react';
import App from './App.tsx';
import { Toaster } from 'sonner';

const samlAuthEnabled: boolean =
  import.meta.env.VITE_APP_SAMLAUTH_ENABLED === 'true';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/setting',
    element: <Setting />,
  },
  {
    path: '/agent-core',
    element: <AgentCorePage />,
  },
  {
    path: '/share/:shareId',
    element: <SharedChatPage />,
  },
  {
    path: '*',
    element: <NotFound />,
  },
];

const router = createBrowserRouter([
  {
    path: '/',
    element: samlAuthEnabled ? (
      <AuthWithSAML>
        <App />
      </AuthWithSAML>
    ) : (
      <AuthWithUserpool>
        <App />
      </AuthWithUserpool>
    ),
    children: routes,
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* eslint-disable-next-line @shopify/jsx-no-hardcoded-content */}
    <React.Suspense fallback={<div>Loading...</div>}>
      <Authenticator.Provider>
        <RouterProvider router={router} />
        <Toaster />
      </Authenticator.Provider>
    </React.Suspense>
  </React.StrictMode>
);
