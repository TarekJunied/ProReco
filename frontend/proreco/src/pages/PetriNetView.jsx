import React from 'react'
import ChooseLayout from '../layout/ChooseLayout';
import PetriNet from '../components/PetriNet';
import LoadingSpinner from '../components/LoadingSpinner';
import { useNavigate } from 'react-router-dom';
import axios from "axios"
import { useState, useEffect } from 'react';

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
    zIndex: 10,
    flexDirection: 'row', // Change from column to row for horizontal layout
    gap: '20px', // Optional: Add some space between each wheel
};
const containerStyle = {
    display: "flex",
    alignItems: 'center', // This centers vertically in the flex container
    justifyContent: 'center', // This centers horizontally in the flex container
    width: '100vw', // Take at least the full width of the viewport
};


const PetriNetView = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionTokenParam = urlParams.get('sessionToken');
    const discoveryAlgorithmParam = urlParams.get('discoveryAlgorithm')
    const [isComputing, setIsComputing] = useState(true);
    const discoveryAlgorithm = decodeURIComponent(discoveryAlgorithmParam);
    const sessionToken = decodeURIComponent(sessionTokenParam);
    const [petriNetData, setPetriNetData] = useState(null);


    const getPetriNetDictionaryFromBackend = (sessionToken, discoveryAlgorithm) => {
        const requestData = {
            sessionToken,
            discoveryAlgorithm
        };
        axios.post("http://localhost:8000/api/requestModel", { requestData })
            .then((response) => {

                console.log(`Successfully received follwowing petri net of ${sessionToken} using ${discoveryAlgorithm}:`);
                console.log(response.data)
                setPetriNetData(response.data);
                setIsComputing(false)


            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
            });
    };

    useEffect(() => {
        // Call the function when the component mounts
        getPetriNetDictionaryFromBackend(sessionToken, discoveryAlgorithm);
    }, []); // Empty dependency array to ensure it runs only once



    return (
        <ChooseLayout>
            <div style={containerStyle}>


                {!isComputing && (
                    <PetriNet windowWidthInVW={0.9} data={petriNetData} />

                )}


            </div>
            {isComputing && (

                <div style={overlayStyle}>

                    <LoadingSpinner text={"Mining..."} />

                </div>
            )
            }
            {isComputing &&
                <div style={{
                    marginBottom: "70vh"
                }} />}







        </ChooseLayout>
    );
}

export default PetriNetView
