import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/backgroundWithoutHelmet.png';
import HelmetComponent from '../components/HelmetComponent';
import "../components/styles/Helmet.css"


const LandingLayout = ({ children }) => {
    return (



        <div style={{ position: "relative" }}>

            <div>

                <div style={{
                    backgroundImage: `url(${backgroundImage})`,
                    backgroundSize: "cover",
                    backgroundPosition: "top",
                    position: "relative",
                    minHeight: "100vh",
                    width: "100vw",
                    zIndex: -1
                }}>

                    <HelmetComponent className="heartbeat-helmet" />

                </div>



            </div>
        </div>

    );
}

LandingLayout.propTypes = {
    children: PropTypes.node,
};

export default LandingLayout;
