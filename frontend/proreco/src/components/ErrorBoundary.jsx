import { Component } from 'react';
import PropTypes from 'prop-types';
import { Navigate } from 'react-router-dom';

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        console.error('Error caught by getDerivedStateFromError:', error);
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error caught by componentDidCatch:', error, errorInfo);
        // You can log the error to an error reporting service
    }

    render() {
        if (this.state.hasError) {
            // You can customize the error message or redirect to a different route
            console.error('ErrorBoundary rendering Navigate to /home');
            return <Navigate to="/" />;
        }

        return this.props.children;
    }
}

ErrorBoundary.propTypes = {
    children: PropTypes.node.isRequired,
};

export default ErrorBoundary;
