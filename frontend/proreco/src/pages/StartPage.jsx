import { useRef } from 'react';
import ChooseLayout from '../layout/ChooseLayout';
import UploadButton from '../components/UploadButton';
import StartButton from '../components/StartButton';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const StartPage = () => {
    const navigate = useNavigate();
    const fileInputRef = useRef(null);

    const handleFileInputChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const formData = new FormData();
            formData.append('xesFile', selectedFile);

            axios
                .post('http://localhost:8000/api/submitLog', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                    withCredentials: true,
                })
                .then((response) => {

                    console.log('File uploaded successfully:', response.data);

                    localStorage.setItem('sessionToken', response.data.sessionToken);
                    navigate(`/ranking?sessionToken=${response.data.sessionToken}`);
                })
                .catch((error) => {
                    console.error('Error uploading file:', error);
                });
        }
    };

    const handleUploadButtonClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center">
            <ChooseLayout>
                <div className="flex flex-col items-center justify-center flex-grow mb-40">
                    <div className="flex flex-col items-center space-y-20 flex-grow">
                        <div className="flex-grow"></div>
                        <div className="w-full">
                            <input
                                type="file"
                                ref={fileInputRef}
                                style={{ display: 'none' }}
                                onChange={handleFileInputChange}
                            />
                            <UploadButton
                                text="Upload Event Log"
                                styles="bg-orange-gradient text-[40px]"
                                onClick={handleUploadButtonClick}
                            />
                        </div>
                        <div className="flex-grow"></div>
                        <div className="w-full">
                            <StartButton
                                text="Choose Existing Event Log"
                                styles="bg-orange-gradient text-[40px]"
                            />
                        </div>
                        <div className="flex-grow"></div>
                        <div className="w-full">
                            <StartButton
                                text="Generate Event Log"
                                styles="bg-orange-gradient text-[40px]"
                            />
                        </div>
                        <div className="flex-grow"></div>
                    </div>
                </div>
            </ChooseLayout>
        </div>
    );
};

export default StartPage;
