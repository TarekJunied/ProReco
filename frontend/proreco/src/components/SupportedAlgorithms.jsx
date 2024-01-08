
import { Link } from 'react-router-dom';
import splitLogo from '../assets/split-logo.png';
import alphaLogo from '../assets/alpha-logo.png';
import ilpLogo from '../assets/ILP-logo.png';
import heuristicLogo from '../assets/heuristic-logo.png';
import inductiveLogo from '../assets/inductive-logo.png';
import inductiveDirectLogo from '../assets/inductive_direct-logo.png';
import inductiveInfrequentLogo from '../assets/inductive_infrequent-logo.png';
import alphaPlusLogo from '../assets/alpha_plus-logo.png';

import './styles/SupportedAlgorithms.css';
import { AlgorithmPortfolio } from '../constants';


const splitUrl = 'https://www.processmining.org/split';
const alphaUrl = 'https://www.processmining.org/alpha';
const ilpUrl = 'https://www.processmining.org/ilp';
const heuristicUrl = 'https://www.processmining.org/heuristic';
const inductiveUrl = 'https://www.processmining.org/inductive';

function generateAlgorithmCaption(discoveryAlgorithm) {
    // Split the algorithm name at underscores
    const parts = discoveryAlgorithm.split('_');

    // Create a caption with two lines if there are two parts
    return parts.length === 2
        ? `${parts[0].toUpperCase()}\n${parts[1]}`
        : discoveryAlgorithm.toUpperCase();
}
function translateAlgoName(algorithmName) {
    let ret;
    switch (algorithmName) {

        case "inductive":
            ret = "IM"
            break;
        case "inductive_direct":
            ret = "IMd"
            break;
        case "inductive_infrequent":
            ret = "IMf"
            break;
        case "alpha_plus":
            ret = "ALPHA +"
            break;
        default:
            ret = algorithmName.toUpperCase()
    }
    return ret;
}

function getAlgorithmLogo(algorithmName) {
    let logo;
    switch (algorithmName) {
        case "split":
            logo = splitLogo;
            break;
        case "alpha":
            logo = alphaLogo;
            break;
        case "ilp", "ILP":
            logo = ilpLogo;
            break;
        case "heuristic":
            logo = heuristicLogo;
            break;
        case "inductive":
            logo = inductiveLogo;
            break;
        case "inductive_direct":
            logo = inductiveDirectLogo;
            break;
        case "inductive_infrequent":
            logo = inductiveInfrequentLogo;
            break;
        case "alpha_plus":
            logo = alphaPlusLogo;
            break;
        default:
            logo = null; // or a default logo if you have one
    }
    return logo;
}



const getAlgoUrl = (discoveryAlgorithm) => {
    let ret = null;

    switch (discoveryAlgorithm) {
        case "alpha":
            ret = alphaUrl;
            break;
        case "ILP":
            ret = ilpUrl;
            break;
        case "split":
            ret = splitUrl;
            break;
        case "inductive":
            ret = inductiveUrl;
            break;
        case "heuristic":
            ret = heuristicUrl;
            break;
        default:
            // Handle the case when the discoveryAlgorithm doesn't match any known algorithms.
            break;
    }

    return ret;
};




const SupportedAlgorithms = () => {
    // Define the URLs you want the images to link to
    const headingStyle = {
        fontSize: "2.7vw",
        fontWeight: 500,
        color: "white"

    }
    const algoDivStyle = {
        display: "flex",
        width: "100%",
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: 'rgba(67, 20, 7, 0.3)',
        borderRadius: "20px",
        padding: "1vw"

    }
    const algoCaptionStyle = {
        fontSize: "1vw",
        fontWeight: "300",
        color: "white"

    }


    const individualAlgoDivStyle = {
        width: "7.5vw",
        margin: "0px",
        padding: "1vw",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    }



    return (
        <div>
            <h1 style={headingStyle}>Supported Algorithms:</h1>
            <div style={algoDivStyle} >
                <ul style={{ display: "flex", flexDirection: "row", }}>
                    {AlgorithmPortfolio.map((discoveryAlgorithm, index) => (


                        // Split the algorithm name at underscores



                        <li key={index}>
                            <Link to={getAlgoUrl(discoveryAlgorithm)} target="_blank" rel="noopener noreferrer">
                                <div style={individualAlgoDivStyle}>
                                    <img src={getAlgorithmLogo(discoveryAlgorithm)} alt={discoveryAlgorithm} id={discoveryAlgorithm} />
                                    <div style={algoCaptionStyle}>
                                        {translateAlgoName(discoveryAlgorithm)}
                                    </div>
                                </div>
                            </Link>
                        </li>

                    ))}

                </ul>
            </div>
        </div >
    );
}

export default SupportedAlgorithms;
