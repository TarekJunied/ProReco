import PropTypes from 'prop-types';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingPage from '../pages/LoadingPage';
import "../index.css"


const uploadButtonStyle = {
    width: "50vw",
    height: "10vh",
    outline: "None",
    borderRadius: "8px",
    color: "white",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: "3vw",
    background: `linear-gradient(157.81deg,
        #FFA000 -43.27%,
        #FF8C00 -21.24%,
        #FF7700 12.19%,
        #FF6300 29.82%,
        #FF4F00 51.94%,
        #BF3604 90.29%)`,
    cursor: "pointer", // Change for an upload button
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
};

// eslint-disable-next-line react/prop-types
const UploadButton = ({ text, onClick }) => {
    const navigate = useNavigate();


    const handleFileUpload = async (event) => {
        const file = event.target.files[0];

        if (file) {
            // Show the loading screen

            // Simulate loading with a timeout (you can replace this with actual upload logic)
            setTimeout(() => {
                // Forward to the next page
                navigate('/ranking'); // Replace with your actual route
            }, 2000); // Adjust the timeout as needed
        }
    };

    return (
        <div>
            <input type="file" accept=".xes" onChange={handleFileUpload} style={{ display: 'none' }} />
            <button
                type="button"
                style={uploadButtonStyle}
                onClick={onClick}
            >
                {text}
            </button>
        </div>
    );
}

UploadButton.propTypes = {
    text: PropTypes.string.isRequired,
    styles: PropTypes.string,
};

export default UploadButton;
