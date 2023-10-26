import PropTypes from 'prop-types';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoadingPage from '../pages/LoadingPage';


// eslint-disable-next-line react/prop-types
const UploadButton = ({ text, styles, onClick }) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];

        if (file) {
            // Show the loading screen
            setLoading(true);

            // Simulate loading with a timeout (you can replace this with actual upload logic)
            setTimeout(() => {
                // Forward to the next page
                navigate('/ranking'); // Replace with your actual route
            }, 2000); // Adjust the timeout as needed
        }
    };

    return (
        <div>
            <div>
                <input type="file" accept=".xes" onChange={handleFileUpload} style={{ display: 'none' }} />
                <button
                    type="button"
                    style={{
                        width: "800px",
                        height: "auto",
                    }}
                    onClick={onClick}
                    className={`w-200 h-100 py-2 px-40 font-bold text-[25px] rounded-[8px] text-primary outline-none ${styles} text-white text-center`}
                >
                    {text}
                </button>
            </div>

            {/* Loading Screen */}
            {loading && (
                <LoadingPage />
            )}
        </div>
    );
}

UploadButton.propTypes = {
    text: PropTypes.string.isRequired,
    styles: PropTypes.string,
};

export default UploadButton;
