
import logo from '../assets/react.svg';

const LoadingPage = () => {
    return (
        <div className="h-screen flex flex-col justify-center items-center bg-dark-gradient-reversed">
            {/* Logo */}
            <img
                src={logo} // Replace with your logo image URL
                alt="Logo"
                className="w-16 h-16 mb-4"
            />

            {/* Loading Text */}
            <p className="text-white text-[40px] font-semibold mb-2" style={{ color: "#D9C4BF" }}>Loading...</p>

            {/* Additional Sentence */}
            <p className="text-[20px] text-gray-200">Patience, young Jedi. The Force is strong with our servers.</p>
        </div>
    );
};

export default LoadingPage;
