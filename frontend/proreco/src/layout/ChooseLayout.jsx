import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';

const ChooseLayout = ({ children }) => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "bottom",
            width: "100vw",
            minHeight: "100vh",
        }}>
            <NavBar />

            {children}


            <Footer />
        </div>
    );
}

ChooseLayout.propTypes = {
    children: PropTypes.node,
};

export default ChooseLayout;
