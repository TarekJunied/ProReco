import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';
import HelmetComponent from '../components/HelmetComponent';
import Hero from '../components/Hero';

const MainLayout = ({ children }) => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            position: "absolute",
            backgroundSize: "cover",
            backgroundPosition: "top",
            minHeight: "100vh",
            width: "100vw"
        }}>


            <NavBar />
            <Hero />

            {children}

            <div style={{ marginBottom: "100vh" }} />
            <Footer />
        </div>
    );
}

MainLayout.propTypes = {
    children: PropTypes.node,
};

export default MainLayout;
