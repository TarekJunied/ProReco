import { useState, useRef } from 'react';
import ChooseLayout from '../layout/ChooseLayout';
import RedirectButton from '../components/RedirectButton';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';


const AfterGeneration = () => {
    const navigate = useNavigate();

    const urlParams = new URLSearchParams(window.location.search);
    const sessionTokenParam = urlParams.get('sessionToken');

    const sessionToken = decodeURIComponent(sessionTokenParam)

    const handleUploadButtonClick = () => {
        return 0
    }



    const handleDownloadButtonClick = () => {
        const url = 'https://proreco.co:8000/api/downloadEventLog';


        axios({
            url,
            method: 'GET',
            responseType: 'blob', // Important for files
            headers: {
                Authorization: sessionToken, // Include the session token in the request headers
            },
        }).then((response) => {
            Swal.close(); // Close the initial Swal once the download starts

            const file = new Blob([response.data], { type: 'application/xml' }); // MIME type for XES files
            const fileURL = window.URL.createObjectURL(file);
            const link = document.createElement('a');
            link.href = fileURL;
            link.setAttribute('download', 'generatedEventLog.xes'); // Set the file name here
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            Swal.fire({
                title: 'Downloaded!',
                text: 'Your file has been downloaded successfully.',
                icon: 'success',
                timer: 3000,
                confirmButtonColor: '#ED4B11',

            });

        }).catch(error => {
            Swal.fire({
                title: 'Failed to Download',
                text: 'There was an issue downloading your file.',
                icon: 'error',
                confirmButtonColor: '#ED4B11',

            });
            console.error("There was an error downloading the file:", error);
        });
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


                <div style={{
                    ...buttonStyle, marginTop: "2vh"
                }}>


                    <RedirectButton
                        text="Download Generated Event Log"
                        onClick={handleDownloadButtonClick}
                    />

                </div>




                <div style={buttonStyle}>


                    <RedirectButton
                        text="Get Recommendations"
                        onClick={() => navigate(`/ranking?sessionToken=${sessionToken}`)}
                    />

                </div>
                <div style={buttonStyle}>

                    <RedirectButton
                        text="Mine Process Model"
                        onClick={() => navigate(`/mine?sessionToken=${sessionToken}`)}
                    />

                </div>

            </div>
        </ChooseLayout >
    );
};

export default AfterGeneration;
