
import reactLogo from '../assets/react.svg'; // Import the logo image
import { Component } from "react";
import Button from "./Button.jsx"
import styles from "../styles.js"
import "./styles/NavBarStyles.css"

class NavBar extends Component {
    state = { clicked: false };

    handleClick = () => {
        this.setState({ clicked: !this.state.clicked })
    }
    render() {
        return (
            <div className="navbar">
                <nav>
                    <a href="www.proreco.com">
                        <img src={reactLogo} alt="React Logo" />

                    </a>
                    <div>
                        <ul id="navbar" className={this.state.clicked ? "#navbar active" : "#navbar"}>
                            <li><a href="index.html" className="active">Home</a> </li>

                            <li><a href="index.html">About</a> </li>
                            <li><a href="index.html">Process Mining</a> </li>
                            <li><a href="index.html">Contact</a> </li>

                            <li><a href="index.html">Source</a> </li>

                            <li> <div className={`justify-between ${styles.flexCenter}`}>
                                <Button text="Get started" styles="bg-orange-gradient" /></div></li>
                        </ul>


                    </div>
                    <div id="mobile" onClick={this.handleClick}>
                        <i id="bar" className={this.state.clicked ? "fas fa-times" : "fas fa-bars"} > </i>
                    </div>

                </nav >
            </div>
        );
    }
}

export default NavBar;