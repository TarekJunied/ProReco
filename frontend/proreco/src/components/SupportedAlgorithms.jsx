
import { Link } from 'react-router-dom';
import splitLogo from '../assets/split-logo.png';
import alphaLogo from '../assets/alpha-logo.png';
import ilpLogo from '../assets/ILP-logo.png';
import heuristicLogo from '../assets/heuristic-logo.png';
import inductiveLogo from '../assets/inductive-logo.png';
import './styles/SupportedAlgorithms.css';
import { AlgorithmPortfolio } from '../constants';


const splitUrl = 'https://www.processmining.org/split';
const alphaUrl = 'https://www.processmining.org/alpha';
const ilpUrl = 'https://www.processmining.org/ilp';
const heuristicUrl = 'https://www.processmining.org/heuristic';
const inductiveUrl = 'https://www.processmining.org/inductive';


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
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: 'rgba(67, 20, 7, 0.3)',
        borderRadius: "20px",
        padding: "1vw"

    }
    const algoCaptionStyle = {
        fontSize: "25px",
        fontWeight: "300",
        color: "white"

    }





    return (
        <div>
            <h1 style={headingStyle}>Supported Algorithms:</h1>
            <div style={algoDivStyle} >
                <ul className="flex space-x-16">
                    {AlgorithmPortfolio.map((discoveryAlgorithm, index) => (
                        <li key={index}>
                            <Link to={getAlgoUrl(discoveryAlgorithm)} target="_blank" rel="noopener noreferrer">
                                <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                                    <img src={getAlgorithmLogo(discoveryAlgorithm)} alt={discoveryAlgorithm} id={discoveryAlgorithm} />
                                    <p style={algoCaptionStyle}>{discoveryAlgorithm.toUpperCase()}</p>
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
