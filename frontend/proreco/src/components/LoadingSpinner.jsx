import React from 'react';
import { ColorRing } from 'react-loader-spinner'; // Import ColorRing component
const textStyle = {
    display: '-webkit-box', // Required for 'WebkitLineClamp'
    WebkitBoxOrient: 'vertical', // Required for 'WebkitLineClamp'
    marginTop: '2vh',
    textAlign: 'center',
    color: "white",
    fontSize: "1.9vw",
    alignSelf: 'center',
    height: '2vh', // Fixed height for the text containeride overflow
    WebkitLineClamp: 2,
}

const LoadingSpinner = ({ text }) => {
    return (
        <div style={{
            display: 'flex',        // Use flexbox for layout
            flexDirection: 'column', // Stack items vertically
            alignItems: 'center',    // Center items horizontally in the container
            justifyContent: 'center', // Center items vertically in the container
        }}>
            <ColorRing
                width="27vw"
                height="27vw"
                wrapperStyle={{ marginBottom: '0vh' }}
                wrapperClass="color-ring-wrapper"
                colors={["#FFA000", "#FF8C00", "#FF7700", "#FF6300", "#FF4F00", "#BF3604"]}
            />

            <div style={{ ...textStyle, marginTop: "-6vh" }}> {/* Decreased from 2vh to 1vh */}
                {text}
            </div>
        </div>
    )
}

export default LoadingSpinner;
