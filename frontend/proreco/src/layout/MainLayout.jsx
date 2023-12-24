import PropTypes from 'prop-types';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
//import Newsletter from '../components/Newsletter';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/backgroundWithoutHelmet.png';
import HelmetComponent from '../components/HelmetComponent';


const MainLayout = ({ children }) => {
    return (
        <div style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "top",
            position: "absolute",
            minHeight: "100vh",
            width: "100vw"
        }}>

            <HelmetComponent />
            <NavBar />
            {children}


            <Footer />
        </div>
    );
}

MainLayout.propTypes = {
    children: PropTypes.node,
};

export default MainLayout;
