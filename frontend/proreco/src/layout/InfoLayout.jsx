import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';

//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';


const InfoLayout = ({ children }) => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            position: "absolute",
            backgroundPosition: "bottom",
            backgroundRepeat: "repeat-y", // Set to repeat vertically
            width: "100vw",
            minHeight: "100vh"
        }} >
            <NavBar />
            {children}


            <Footer />
        </div>
    );
}

InfoLayout.propTypes = {
    children: PropTypes.node,
};

export default InfoLayout;
