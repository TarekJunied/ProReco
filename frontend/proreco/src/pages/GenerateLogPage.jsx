
import ChooseLayout from '../layout/ChooseLayout'
import GenerateSlider from "../components/GenerateSlider"
import LoadingSpinner from '../components/LoadingSpinner';
import { useState, useEffect } from "react";
import RedirectButton from '../components/RedirectButton';
import Swal from 'sweetalert2';
import ProgressWheel from "../components/ProgressWheel";
import axios from "axios"
import { useNavigate } from "react-router-dom";

const rankSliderConatinerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    marginBottom: "8vh"
}

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
const parameterList = [
    "andBranches",
    "xorBranches",
    "loopWeight",
    "singleActivityWeight",
    "skipWeight",
    "sequenceWeight",
    "andWeight",
    "xorWeight",
    "maxDepth",
    "dataObjectProbability"
    , "numberOfTraces"
];
const parameterRange = {
    "andBranches": { "min": 0, "max": 10, "step": 1, "init": 5 },
    "xorBranches": { "min": 0, "max": 10, "step": 1, "init": 5 },
    "loopWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.1 },
    "singleActivityWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.2 },
    "skipWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.1 },
    "sequenceWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.7 },
    "andWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.3 },
    "xorWeight": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.3 },
    "maxDepth": { "min": 1, "max": 5, "step": 1, "init": 3 },
    "dataObjectProbability": { "min": 0.0, "max": 1.0, "step": 0.01, "init": 0.1 },
    "numberOfTraces": { "min": 1, "max": 3000, "step": 1, "init": 300 }
};

const buttonStyle = {
    display: 'flex',        // Equivalent to 'flex'
    width: '100%',          // Equivalent to 'w-full'
    justifyContent: 'center',
    marginBottom: "15vh"
};
const progressWheelStyle = {
    width: '150px', // Set a fixed width
    height: '150px', // Set a fixed height
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
};


const GenerateLogPage = () => {

    const initialSliderValues = parameterList.map(parameter => parameterRange[parameter].init);
    const [isComputing, setIsComputing] = useState(false)
    const [sliderValues, setSliderValues] = useState(initialSliderValues);


    const navigate = useNavigate();


    const sessionToken = localStorage.getItem('sessionToken');
    const mainDivStyle = {
        display: 'flex',                 // Equivalent to 'flex'
        flexDirection: 'column',        // Equivalent to 'flex-col'
        alignItems: 'center',           // Equivalent to 'items-center'
        justifyContent: 'center',       // Equivalent to 'justify-center'

    };


    const handleButtonClick = () => {
        setIsComputing(true)

        const requestData = {};
        for (let i = 0; i < parameterList.length; i++) {
            requestData[parameterList[i]] = sliderValues[i];
        }
        console.log("Formatted Request Data:", requestData);


        console.log({ sliderValues })

        axios.post("http://localhost:8000/api/generateLog", { requestData })
            .then((response) => {

                console.log('Successfully generated event log ! ')


                localStorage.setItem('sessionToken', response.data.sessionToken);


                Swal.fire({
                    title: 'Success ! Event Log Generated.',
                    confirmButtonColor: '#BF3604',
                    imageUrl: './src/assets/cuteIcon.png',
                    imageWidth: 250,
                    imageHeight: 250,
                    imageAlt: 'Custom image',
                    animation: true

                }).then(() => {

                    navigate(`/afterGeneration?sessionToken=${encodeURIComponent(response.data.sessionToken)}`);


                });
            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);

            });

    }

    const handleSliderChange = (index, value) => {
        // Update the slider values in the state
        const updatedValues = [...sliderValues];
        updatedValues[index] = value;
        setSliderValues(updatedValues);
    };
    return (
        <ChooseLayout>
            <div style={{ mainDivStyle }}>


                {isComputing && (

                    <div style={overlayStyle}>

                        <LoadingSpinner text={"Generating..."} />

                    </div>
                )
                }


                {!isComputing && (



                    <div style={rankSliderConatinerStyle}>
                        {parameterList.map((parameter, index) => (
                            <div key={index} style={{ marginBottom: "4vh", width: "80vw" }}>
                                <GenerateSlider
                                    min={parameterRange[parameter].min}
                                    max={parameterRange[parameter].max}
                                    value={sliderValues[index]}
                                    onChange={(value) => handleSliderChange(index, value)}
                                    step={parameterRange[parameter].step}
                                    label={parameter}
                                />
                            </div>
                        ))}



                    </div>


                )}
                {isComputing &&
                    <div style={{
                        marginBottom: "70vh"
                    }} />}

                {!isComputing &&

                    <div style={buttonStyle}>
                        <RedirectButton text="Generate Event Log" onClick={handleButtonClick} />
                    </div>
                }
            </div>

        </ChooseLayout>
    )
}

export default GenerateLogPage
