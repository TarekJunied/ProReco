
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import "../components/styles/LandingPage.css";
import backgroundImage from '../assets/plainBackground.png';

const ChooseLayout = ({ children }) => {



    return (
        <div style={{
            display: 'flex',           // Set to flex to enable flexbox layout
            flexDirection: 'column',
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: "cover",
            backgroundPosition: "bottom",
            position: "absolute",
            width: "100vw",
            minHeight: "100vh",
            backgroundRepeat: "repeat",
            overflowX: "hidden" // Prevent horizontal scrolling

        }}>
            <div style={{
                width: '100%',
                marginBottom: "8vh"
            }}>
                <NavBar />
            </div>





            {children}


            <Footer ></Footer>



        </div>
    );
}

export default ChooseLayout;
