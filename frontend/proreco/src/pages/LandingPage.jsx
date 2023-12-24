
import "../components/styles/LandingPage.css"
import MainLayout from '../layout/MainLayout';
import Hero from "../components/Hero";
import SupportedAlgorithms from "../components/SupportedAlgorithms";


const LandingPage = () => {
    return (
        <MainLayout>

            <Hero />
            <SupportedAlgorithms />
        </MainLayout>



    );
}
export default LandingPage;
