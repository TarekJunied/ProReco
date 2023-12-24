import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


const textStyle = {
    display: '-webkit-box', // Required for 'WebkitLineClamp'
    WebkitBoxOrient: 'vertical', // Required for 'WebkitLineClamp'
    marginTop: '2vh',
    textAlign: 'center',
    color: "white",
    fontSize: "1.9vw",
    alignSelf: 'center',
    height: '6vh', // Fixed height for the text containeride overflow
    WebkitLineClamp: 2,
}

const progressBarStyle = {
    display: 'flex',               // Make this a flex container
    flexDirection: 'column',       // Arrange children in a column
    alignItems: 'center',          // Center children horizontally
    justifyContent: 'center',      // Center children vertically
    width: '20vw',
    height: "10vw",
    marginBottom: '4vh' // Add margin to ensure spacing remains consistent

}



const ProgressWheel = ({ percentage, text }) => {
    const gradientId = 'progressGradient';
    return (
        <div style={{ progressBarStyle }}>
            <svg style={{ width: 0, height: 0 }}>
                <defs>
                    <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#DB4400" /> {/* Dark Orange Start */}
                        <stop offset="100%" stopColor="#FF8B00" /> {/* Bright Orange End */}
                    </linearGradient>
                </defs>
            </svg>
            <div style={{
                marginBottom: "4vh",
                width: "17vw",
            }}>

                <CircularProgressbar
                    value={percentage}
                    text={`${percentage}%`}
                    styles={buildStyles({
                        textSize: '20px',
                        pathColor: `url(#${gradientId})`, // Apply the gradient here
                        textColor: '#FF6300',
                        trailColor: '#d6d6d6',
                        backgroundColor: '#3e98c7',
                    })} />
            </div>
            <div style={textStyle} >
                {text}
            </div>
        </div>
    );
};

export default ProgressWheel;
