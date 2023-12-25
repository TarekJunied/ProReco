import PropTypes from 'prop-types';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingPage from '../pages/LoadingPage';
import "../index.css"


const buttonStyle = {
    width: '100%', // Make the button fill its container
    outline: "None",
    borderRadius: "8px",
    color: "white",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: "2vw",
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
    alignItems: "center",
    padding: "0.5vw"
};

// eslint-disable-next-line react/prop-types
const NextFeature = ({ text, onClick }) => {

    return (
        <div>
            <button
                type="button"
                style={buttonStyle}
                onClick={onClick}
            >
                {text}

            </button>
        </div>
    );
}


export default NextFeature;
