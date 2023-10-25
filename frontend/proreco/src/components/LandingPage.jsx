import NavBar from './NavBar';
import Hero from './Hero'
import "./styles/LandingPage.css"
import styles from "../styles.js"


const LandingPage = () => {
    return (

        <div className="landingpage">
            <NavBar />
            <div className={`${styles.flexStart} mb-40`}>
                <div className={`${styles.boxWidth}`}>
                    <Hero />
                </div>

            </div>

        </div >


    );
}
export default LandingPage;
