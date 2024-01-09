import React from 'react'
import ChooseLayout from '../layout/ChooseLayout';
import { AlgorithmPortfolio } from "../constants";
import { useNavigate } from 'react-router-dom';
import { Tooltip } from 'react-tooltip'
import AlgorithmView from '../components/AlgorithmView';

const MinePage = () => {
    const navigate = useNavigate();

    const urlParams = new URLSearchParams(window.location.search);
    const sessionTokenParam = urlParams.get('sessionToken');
    const sessionToken = decodeURIComponent(sessionTokenParam);
    const toolTipStyle = {
        fontSize: "2vw"
    }

    const handleClick = (discoveryAlgorithm) => () => {
        navigate(`/viewPetriNet?sessionToken=${sessionToken}&discoveryAlgorithm=${discoveryAlgorithm}`);
    }
    const headingStyle = {

        alignSelf: "center",
        color: "white",
        fontSize: "5vw"

    }
    const tooltipTexts = {
        "alpha": "Usually produces simple models",
        "alpha_plus": "Usually produces simple models",
        "inductive": "Perfect Fitness, Medium Precision",
        "ILP": "Perfect Fitness, Usually complex models",
        "heuristic": "High Fitness High Precision",
        "split": "High Fitness Perfect Precision",
        "inductive_infrequent": "Perfect Fitness, Medium Precision",
        "inductive_direct": "Perfect Fitness, Medium Precision"
    }




    return (

        <ChooseLayout>
            <h1 style={headingStyle}>Choose your Algorithm ⛏️ </h1>
            <div className="flex justify-center w-screen mt-10">
                <div className="flex-row">
                    {AlgorithmPortfolio.map((DiscoveryAlgorithm, index) => (
                        <div key={index} style={{
                            marginTop: index === 0 ? "0" : "5vh",
                            width: "50vw",
                            cursor: "pointer" // add top margin for all but the first item
                        }}>
                            <a
                                data-tooltip-id={`${DiscoveryAlgorithm}sToolTip`}
                                data-tooltip-html={tooltipTexts[DiscoveryAlgorithm]}
                                data-tooltip-place="top"
                                onClick={handleClick(DiscoveryAlgorithm)}

                            >
                                <AlgorithmView
                                    algorithmName={DiscoveryAlgorithm} />
                            </a>

                            <Tooltip id={`${DiscoveryAlgorithm}sToolTip`}
                                style={toolTipStyle}
                                place="top" />
                        </div>
                    ))}

                </div>
            </div>
        </ChooseLayout>
    );
}

export default MinePage;
