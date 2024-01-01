import React from 'react';

// eslint-disable-next-line react/prop-types
const ClickableAlgo = ({ handleClick, discoveryAlgorithm }) => {
    return (
        <div>
            <div
                className="text-center text-bold text-white text-[30px] flex-row flex justify-center mb-10 cursor-pointer"
                onClick={handleClick}
                role="button"
                tabIndex={0}
            >
                <div className="uppercase">{discoveryAlgorithm}</div>
            </div>
        </div>
    );
}

export default ClickableAlgo;
