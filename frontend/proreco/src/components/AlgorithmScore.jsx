import React from 'react'

import splitLogo from '../assets/split-logo.png';
import alphaLogo from '../assets/alpha-logo.png';
import ilpLogo from '../assets/ILP-logo.png';
import heuristicLogo from '../assets/heuristic-logo.png';
import inductiveLogo from '../assets/inductive-logo.png';
import { Tooltip } from 'react-tooltip'

function getEmoji(placement) {
    switch (placement) {
        case 1:
            return '🥇'; // Gold Medal for first place
        case 2:
            return '🥈'; // Silver Medal for second place
        case 3:
            return '🥉'; // Bronze Medal for third place
        default:
            return '🏅'; // Other generic medal or symbol for other places
    }
}

function getPlacementStyle(placement) {
    switch (placement) {
        case 1: // Gold
            return {
                boxShadow: '0 0 0.5vh gold, 0 0 1vh gold, 0 0 2vh goldenrod, 0 0 3vh DarkGoldenRod',
                background: 'linear-gradient(145deg, gold, goldenrod)',
                border: '0.5vw solid DarkGoldenRod' // Gold border
            };
        case 2: // Silver
            return {
                boxShadow: '0 0 0.5vh silver, 0 0 1vh silver, 0 0 2vh lightgrey, 0 0 3vh grey',
                background: 'linear-gradient(145deg, silver, darkgray)',
                border: '0.5vw solid silver' // Silver border
            };
        case 3: // Bronze
            return {
                boxShadow: '0 0 8px darkorange, 0 0 1vh peru, 0 0 20px sienna, 0 0 25px saddlebrown',
                background: 'linear-gradient(145deg, #cd7f32, #8c4b2a)', // using hex for specific bronze shades
                border: '0.5vw solid #cd7f32' // Bronze border
            };
        default:
            return {
                border: '0.5vw solid #FF7700' // Default border
            };
    }
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
        case "ilp":
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
    justifyContent: 'space-between', // Push items to either end

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




const AlgorithmScore = ({ algorithmName, algorithmScore, placement }) => {

    const placementStyle = getPlacementStyle(placement);

    // Merge base boxStyle with placementStyle
    const combinedStyle = { ...boxStyle, ...placementStyle };



    return (
        <div style={combinedStyle}>
            <div style={emojiStyle}>
                {getEmoji(placement)}
            </div>
            <div style={overlayStyle}></div> {/* Overlay Div */}

            <div style={textStyle}>
                {capitalizeAlgorithmName(algorithmName)}
            </div>
            <div style={scoreStyle}>
                {algorithmScore}
            </div>


        </div >
    )
}

export default AlgorithmScore
