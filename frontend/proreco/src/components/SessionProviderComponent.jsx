// SessionProvider.js

import { SessionProvider } from 'react-session';

// eslint-disable-next-line react/prop-types
function SessionProviderComponent({ children }) {
    return (
        <SessionProvider>
            {children}
        </SessionProvider>
    );
}

export default SessionProviderComponent;
