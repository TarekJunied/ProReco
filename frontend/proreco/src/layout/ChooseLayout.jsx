import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/background.png';

const MainLayout = ({ children }) => {
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

            <Newsletter />
            <Footer />
        </div>
    );
}

MainLayout.propTypes = {
    children: PropTypes.node,
};

export default MainLayout;
