import { useState, useRef } from 'react';
import ChooseLayout from '../layout/ChooseLayout';
import UploadButton from '../components/UploadButton';
import StartButton from '../components/StartButton';
import ProgressWheel from '../components/ProgressWheel';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import RedirectButton from "../components/RedirectButton"


const StartPage = () => {
    const navigate = useNavigate();
    const fileInputRef = useRef(null);
    const [uploadProgress, setUploadProgress] = useState(0); // Add state for tracking upload progress
    const [isUploading, setIsUploading] = useState(false); // State to track if upload is in progress
    const overlayStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 10
    };



    const handleFileInputChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const formData = new FormData();
            formData.append('xesFile', selectedFile);

            setIsUploading(true);
            axios
                .post("https://proreco.co:8000/api/submitLog", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    withCredentials: true,
                    onUploadProgress: (progressEvent) => {
                        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                        setUploadProgress(percentCompleted); // Update the upload progress
                    },
                })
                .then((response) => {

                    console.log('File uploaded successfully:', response.data);
                    localStorage.setItem('sessionToken', response.data.sessionToken);


                    Swal.fire({
                        title: 'Event log uploaded succesfully',
                        confirmButtonColor: '#BF3604',
                        imageUrl: './src/assets/cuteIcon.png',
                        imageWidth: 250,
                        imageHeight: 250,
                        imageAlt: 'Custom image',
                        animation: true

                    }).then(() => {
                        // This code will execute after Swal alert is closed
                        closeModalAndNavigate(`/ranking?sessionToken=${response.data.sessionToken}`);
                    });
                })
                .catch((error) => {
                    console.error('Error uploading file:', error);
                });
        }
    };

    const closeModalAndNavigate = (url) => {
        setIsUploading(false);
        navigate(url);
    };

    const handleUploadButtonClick = () => {
        fileInputRef.current.click();
    };


    const buttonStyle = {
        display: 'flex',        // Equivalent to 'flex'
        width: '100%',          // Equivalent to 'w-full'
        justifyContent: 'center',
        marginBottom: "15vh"
    };

    const buttonDivStyle = {
        display: 'flex',                 // Equivalent to 'flex'
        flexDirection: 'column',        // Equivalent to 'flex-col'
        alignItems: 'center',           // Equivalent to 'items-center'
        justifyContent: 'center',       // Equivalent to 'justify-center'

    };


    return (
        <ChooseLayout>
            <div style={buttonDivStyle}>


                {!isUploading &&
                    (<div style={{
                        ...buttonStyle, marginTop: "2vh"
                    }}>
                        <input
                            type="file"
                            ref={fileInputRef}
                            style={{ display: 'none' }}
                            onChange={handleFileInputChange}
                        />

                        <UploadButton
                            text="Upload Event Log"
                            onClick={handleUploadButtonClick}
                        />

                    </div>)}



                {!isUploading &&
                    (<div style={buttonStyle}>


                        <RedirectButton
                            text="Generate Event Log"
                            onClick={() => navigate("/generateLog")}
                        />

                    </div>)}
                {!isUploading &&
                    (<div style={buttonStyle}>

                        <RedirectButton
                            text="Choose Existing Event Log"
                            onClick={() => navigate("/generateLog")}
                        />

                    </div>)}
                {isUploading &&
                    <div style={{
                        marginBottom: "70vh"
                    }} />}

                {
                    isUploading && (
                        <div style={overlayStyle}>
                            <ProgressWheel percentage={uploadProgress} text="Uploading..." />
                        </div>
                    )
                }
            </div>
        </ChooseLayout >
    );
};

export default StartPage;
