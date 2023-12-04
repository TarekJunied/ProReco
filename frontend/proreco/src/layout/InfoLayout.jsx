import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';
import InfoBox from '../components/InfoBox';

const InfoLayout = ({ children }) => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "bottom",
            width: "100vw",
            minHeight: "100vh",
            position: "relative"
        }} >
            <NavBar />
            <InfoBox />
            {children}
            <InfoBox />


            <Footer />
        </div>
    );
}

InfoLayout.propTypes = {
    children: PropTypes.node,
};

export default InfoLayout;
