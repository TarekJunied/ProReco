
import "../components/styles/LandingPage.css"
import MainLayout from '../layout/MainLayout';
import Hero from "../components/Hero";
import SupportedAlgorithms from "../components/SupportedAlgorithms";
import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';
import HelmetComponent from '../components/HelmetComponent';
import TrailerVideo from "../components/TrailerVideo";


const LandingPage = () => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            position: "absolute",
            backgroundSize: "cover",
            backgroundPosition: "top",
            minHeight: "265vh",
            width: "100vw",
            backgroundRepeat: "repeat",
        }}>

            <div style={{
                display: "flex",
                flexDirection: "column"

            }}>

                <div style={{
                }}>
                    <NavBar />

                </div>



                <div style={{
                    position: "absolute",
                    top: "20vh",
                    left: "20vw",

                }}>
                    <Hero />
                </div>

                <div
                    style={{
                        position: "absolute",
                        top: "85vh",
                        left: "20vw",
                        width: "62vw"

                    }}>

                    <SupportedAlgorithms />

                </div>

                <div
                    style={{
                        position: "absolute",
                        top: "120vh",
                        left: "15vw",
                        width: "70vw",
                        height: "50vw"
                    }}

                >
                    <TrailerVideo />
                </div>


                <div
                    style={{
                        position: "absolute",
                        top: "220vh",
                        left: "0vw",
                        width: "100%"

                    }}

                >
                    <Footer />

                </div>


            </div>
        </div>


    );
}
export default LandingPage;
