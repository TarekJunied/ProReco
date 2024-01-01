import React from 'react';
import './styles/Helmet.css'; // Make sure to import the CSS file
import helmetImage from '../assets/helmet.png'; // Update with the path to your image

function HelmetComponent() {
    return (
        <div>
            <img src={helmetImage} alt="Animated Helmet" className="heartbeat-helmet" />
        </div>
    );
}

export default HelmetComponent;
