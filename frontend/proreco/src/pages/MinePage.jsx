import React from 'react'
import ChooseLayout from '../layout/ChooseLayout';
import PetriNet from '../components/PetriNet';
import StartButton from '../components/StartButton';
import { AlgorithmPortfolio } from "../constants";
import ClickableAlgo from '../components/ClickableAlgo';
import { useNavigate } from 'react-router-dom';

const MinePage = () => {
    const navigate = useNavigate();

    const urlParams = new URLSearchParams(window.location.search);
    const sessionTokenParam = urlParams.get('sessionToken');
    const sessionToken = decodeURIComponent(sessionTokenParam);

    const handleClick = (discoveryAlgorithm) => () => {
        navigate(`/viewPetriNet?sessionToken=${sessionToken}&discoveryAlgorithm=${discoveryAlgorithm}`);
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center">
            <ChooseLayout>
                <div className="flex flex-col items-center justify-center flex-grow mb-40">
                    <div className="flex flex-col items-center space-y-20 flex-grow">
                        {AlgorithmPortfolio.map((discoveryAlgorithm, index) => (
                            <div className="flex-col" key={index}>
                                <ClickableAlgo handleClick={handleClick(discoveryAlgorithm)} discoveryAlgorithm={discoveryAlgorithm} ></ClickableAlgo>
                            </div>
                        ))}
                    </div>
                </div>
            </ChooseLayout>
        </div>
    );
}

export default MinePage;
