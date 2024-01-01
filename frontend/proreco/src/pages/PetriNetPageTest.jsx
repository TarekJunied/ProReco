import React from 'react'
import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';
import HelmetComponent from '../components/HelmetComponent';
import AlgorithmScore from '../components/AlgorithmScore';
// Creat

const PetriNetPageTest = () => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "bottom",
            position: "absolute",
            minHeight: "100vh",
            width: "100vw"
        }}>
            <div style={{
                width: '100%',
                marginBottom: "8vh"
            }}>
                <NavBar />
            </div>

            <div style={{ width: "40%", marginTop: "40px" }}>
                {/* Insert the PetriNetComponent where you want the Petri net to appear */}
                <PetriNetComponent />
            </div>



            <Footer />



        </div >
    )
}


export default PetriNetPageTest