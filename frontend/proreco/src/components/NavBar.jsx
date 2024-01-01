import { Component } from "react";
import { Link } from "react-router-dom";
import prorecoLogo from '../assets/pr.png';
import { NavLink } from "react-router-dom"; // import NavLink

import Logo from "./Logo.jsx"
import Button from "./Button.jsx";
import styles from "../styles.js";
import "./styles/NavBarStyles.css";

const buttonStyle = {
    padding: '1rem 1.5rem', // Assuming py-4 and px-6 are 1rem and 1.5rem respectively
    fontWeight: "400",
    fontSize: '1.5vw', // Directly taken from text-[25px]
    borderRadius: '8px', // Directly taken from rounded-[8px]
    color: 'white', // text-white sets the text color
    outline: 'none' // outline-none removes the outline
};




class NavBar extends Component {
    state = { clicked: false };

    handleClick = () => {
        this.setState({ clicked: !this.state.clicked });
    }

    render() {
        return (

            <div>



                <ul id="navbar" className={this.state.clicked ? "navbar active" : "navbar"} style={{ marginTop: "2vh" }} >

                    <div style={{ display: 'flex', alignItems: 'center', height: "7vh", position: "absolute", left: "1%", marginTop: "0.5vh" }}>
                        <Logo />
                    </div>

                    <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
                    <li><NavLink to="/about" activeClassName="active">About</NavLink></li>
                    <li><NavLink to="/process-mining" activeClassName="active">Process Mining</NavLink></li>
                    <li><NavLink to="/contact" activeClassName="active">Contact</NavLink></li>
                    <li><NavLink to="/source" activeClassName="active">Source</NavLink></li>
                    <li>
                        <div className={`justify-between ${styles.flexCenter}`}>
                            <Button
                                text="Get started"
                                style={{
                                    ...buttonStyle,
                                    background: "linear-gradient(157.81deg,#FFA000 -43.27%,#FF8C00 -21.24%,#FF7700 12.19%,#FF6300 29.82%,#FF4F00 51.94%,#BF3604 90.29%)"
                                }}
                            />
                        </div>
                    </li>

                </ul>
            </div>


        );
    }
}

export default NavBar;
