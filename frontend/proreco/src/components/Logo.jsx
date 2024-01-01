import React from 'react'
import { Component } from "react";
import { Link } from "react-router-dom";
import prorecoLogo from '../assets/pr.png';
import "./styles/NavBarStyles.css";



const Logo = () => {
    return (
        <div style={{ height: "100%" }}>
            <Link to="/">
                <img src={prorecoLogo} alt="ProReco Logo" style={{
                    height: "100%", width: "auto",
                    objectFit: "contain"
                }} />
            </Link>
        </div>
    )
}

export default Logo
