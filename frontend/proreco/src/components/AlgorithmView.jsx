import React from 'react'

import splitLogo from '../assets/split-logo.png';
import alphaLogo from '../assets/alpha-logo.png';
import ilpLogo from '../assets/ILP-logo.png';
import heuristicLogo from '../assets/heuristic-logo.png';
import inductiveLogo from '../assets/inductive-logo.png';
import { Tooltip } from 'react-tooltip'



function getImageSize(algorithmName) {
    var style;
    switch (algorithmName) {
        case "split":
            style = {
                width: "20%",
                height: "20%"
            }
            break;
        case "alpha":
            style = {
                width: "20%",
                height: "20%"
            };
            break;
        case "ilp":
            style = {
                width: "20%",
                height: "20%"
            }
            break;
        case "heuristic":
            style = {
                width: "20%",
                height: "20%"
            }
            break;
        case "inductive":
            style = {
                width: "20%",
                height: "20%"
            }
            break;
        default:
            style = {
                width: "20%",
                height: "20%"
            }
    }
    return style;
}

const capitalizeAlgorithmName = (algorithmName) => {
    return algorithmName.charAt(0).toUpperCase() + algorithmName.slice(1);

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
        default:
            logo = null; // or a default logo if you have one
    }
    return logo;
}


const boxStyle = {
    borderRadius: "1vw",
    display: "flex",
    flexDirection: "row",
    alignItems: 'center',
    position: 'relative',
    justifyContent: 'space-between',
    boxShadow: '0 0 0.5vh rgba(255, 99, 0, 0.8), 0 0 1vh rgba(255, 99, 0, 0.8), 0 0 0.5vh rgba(255, 215, 0, 0.8), 0 0 2vh rgba(139, 0, 0, 0.8)',
    background: 'linear-gradient(145deg, #BF3604 51.94%, #8B0000 90.29%)',
    border: '0.5vw solid #8B0000' // #FF6300 border


}
const overlayStyle = {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    opacity: 0.2, // Adjust for desired transparency, lower is more transparent
    borderRadius: "inherit", // Ensures the overlay has the same border radius as the parent
}


const imageStyle = {
    height: 'auto',
    marginRight: "2vw"
}
const textStyle = {
    color: "white",
    fontSize: "5vw",
    marginRight: "3vw"
}
const emojiStyle = {
    fontSize: "5vw",
    marginRight: "1vw"
}
const scoreStyle = {
    color: "white",
    fontSize: "4vw",
}




const AlgorithmView = ({ algorithmName }) => {


    // Merge base boxStyle with placementStyle



    return (
        <div style={boxStyle}>
            <div style={{ ...imageStyle, ...getImageSize(algorithmName) }}>
                <img src={getAlgorithmLogo(algorithmName)} />
            </div>
            <div style={overlayStyle}></div> {/* Overlay Div */}

            <div style={textStyle}>
                {capitalizeAlgorithmName(algorithmName)}
            </div>
            <div style={scoreStyle}>
            </div>
        </div >
    )
}

export default AlgorithmView
