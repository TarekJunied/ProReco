import React from "react";
import Button from "./Button.jsx";
import { useNavigate } from "react-router-dom";


const heroTextDivStyle = {
    flex: 1,
    alignItems: 'flex-start',
    flexDirection: 'column',
    marginBottom: "4vh"
};
const heroHeadingStyle = {
    fontWeight: "600",
    fontSize: "5.7vw",
    color: "white",
    lineHeight: "5vw",
    marginBottom: "1.25vh"
}
const heroParagraphStyle = {
    fontWeight: 'normal', // or could use 400 for the numerical value
    fontSize: '1.25rem',
    color: 'white',
};
const buttonDivStyle = {
    display: "flex",
    flexDirection: "row",
    columnGap: "5vw",
    width: "100%"

}
const buttonStyle = {
    padding: '1rem 1.5rem', // Assuming py-4 and px-6 are 1rem and 1.5rem respectively
    fontWeight: "400",
    fontSize: '1.5vw', // Directly taken from text-[25px]
    borderRadius: '8px', // Directly taken from rounded-[8px]
    color: 'white', // text-white sets the text color
    outline: 'none' // outline-none removes the outline
};


const Hero = () => {
    const navigate = useNavigate();

    const handleClickNavigate = (page) => {
        navigate(page);
    };

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
        }}>
            <div style={heroTextDivStyle}>
                <h1 style={heroHeadingStyle}>
                    Unlock The
                </h1>
                <h1 style={heroHeadingStyle}>
                    <span className="text-gradient">Real Power</span> {""}
                </h1>
                <h1 style={heroHeadingStyle}>
                    Of Process
                </h1>
                <h1 style={heroHeadingStyle}>
                    Discovery
                </h1>
                <p style={heroParagraphStyle}>
                    One of the world&rsquo;s most sophisticated
                    <br />
                    recommender systems for
                    discovery algorithms.
                </p>
            </div>
            <div style={buttonDivStyle}>
                <Button text="Get started" style={{
                    ...buttonStyle, background: "linear-gradient(157.81deg,#FFA000 -43.27%,#FF8C00 -21.24%,#FF7700 12.19%,#FF6300 29.82%,#FF4F00 51.94%,#BF3604 90.29%)"
                }} onClick={() => handleClickNavigate("start")} />
                <Button text="Learn more" style={{ ...buttonStyle, background: "#401010" }} onClick={() => handleClickNavigate("processmining")} />
            </div>
        </div>
    );
};

export default Hero;
