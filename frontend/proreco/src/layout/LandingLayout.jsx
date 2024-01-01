import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/backgroundWithoutHelmet.png';
import HelmetComponent from '../components/HelmetComponent';
import "../components/styles/Helmet.css"


const LandingLayout = ({ }) => {

    const imageUrl = '../public/cuteIcon.png'
    return (
        <div>
            <img src={imageUrl} alt="Your Image" />
        </div>

    );
}

export default LandingLayout;
