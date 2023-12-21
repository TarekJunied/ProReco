import React from 'react'
import ChooseLayout from '../layout/ChooseLayout';
import PetriNet from '../components/PetriNet';
import StartButton from '../components/StartButton';
import { AlgorithmPortfolio } from "../constants";
import ClickableAlgo from '../components/ClickableAlgo';
import { useNavigate } from 'react-router-dom';
import axios from "axios"
import { useState, useEffect } from 'react';


const PetriNetView = () => {
    const navigate = useNavigate();
    const urlParams = new URLSearchParams(window.location.search);
    const sessionTokenParam = urlParams.get('sessionToken');
    const discoveryAlgorithmParam = urlParams.get('discoveryAlgorithm')

    const discoveryAlgorithm = decodeURIComponent(discoveryAlgorithmParam);
    const sessionToken = decodeURIComponent(sessionTokenParam);
    const [petriNetData, setPetriNetData] = useState(null);

    const handleClick = (discoveryAlgorithm) => {


        navigate(`/viewPetriNet?sessionToken=${sessionToken}&discoveryAlgorithm=${discoveryAlgorithm}`);

    }
    const getPetriNetDictionaryFromBackend = (sessionToken, discoveryAlgorithm) => {
        const requestData = {
            sessionToken,
            discoveryAlgorithm
        };
        axios.post("http://localhost:8000/api/requestModel", { requestData })
            .then((response) => {

                console.log(`Successfully sent post request for petri net of ${sessionToken} and using ${discoveryAlgorithm}:`);
                setPetriNetData(response.data);


                // maybe clean the data
            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
            });
    };
    const renderPetriNet = () => {
        if (petriNetData) {
            // Render your PetriNet component or any other components
            // For example:

            return <PetriNet paperHeight={400} paperWidth={800} data={petriNetData} />;

        }
        return <p>Loading Petri Net...</p>;
    };

    useEffect(() => {
        // Call the function when the component mounts
        getPetriNetDictionaryFromBackend(sessionToken, discoveryAlgorithm);
    }, []); // Empty dependency array to ensure it runs only once



    return (
        <div className="min-h-screen flex flex-col items-center justify-center">
            <ChooseLayout>
                <div className="flex flex-col items-center justify-center flex-grow mb-40">
                    <p>{renderPetriNet()}</p>
                </div>
            </ChooseLayout>
        </div>
    );
}

export default PetriNetView
