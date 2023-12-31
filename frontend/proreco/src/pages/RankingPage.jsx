import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"
import ChooseLayout from "../layout/ChooseLayout"
import RankSlider from "../components/RankSlider"
import RedirectButton from "../components/RedirectButton";
import { measures } from "../constants"
import Swal from 'sweetalert2';
import ProgressWheel from "../components/ProgressWheel";
import { SliderValueLabel } from "@mui/material";
import LabeledSlider from "../components/LabeledSlider";

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

const progressWheelStyle = {
    width: '150px', // Set a fixed width
    height: '150px', // Set a fixed height
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
};





const RankingPage = () => {
    const sessionToken = localStorage.getItem('sessionToken');
    const [progressState, setProgressState] = useState(0);
    const [featureName, setFeatureName] = useState("No features yet");
    const [parsePercentage, setParsePercentage] = useState(0);
    const [featurePercentage, setFeaturePrecentage] = useState(0);
    const [predictPecentage, setPredictPercentage] = useState(0);
    const [isComputing, setIsComputing] = useState(0);

    const navigate = useNavigate();

    let pollingInterval = null;


    const startPolling = () => {
        pollingInterval = setInterval(pollProgress, 50); // Poll every 1 second
    };


    const pollProgress = () => {
        const requestData = { sessionToken };

        axios.post('https://proreco.co:8000/api/progress', { requestData })
            .then(response => {
                // Assuming response.data contains the progress information
                console.log("received this data from the backend");
                console.log(response.data)
                setProgressState(response.data.state);
                if (response.data.state == "parsing") {
                    setParsePercentage(response.data.parse_progress)
                }
                if (response.data.state == "featuring") {
                    setParsePercentage(100)
                    setFeatureName(response.data.current_feature_name);
                    setFeaturePrecentage(response.data.feature_progress);
                }
                if (response.data.state == "predicting") {
                    setFeaturePrecentage(100);
                    setPredictPercentage(100);
                }


                if (response.data.state == "done") {
                    clearInterval(pollingInterval); // Stop polling when task is complete
                    setIsComputing(false); // Set isComputing to false when the task is done

                }
            })
            .catch(error => {
                console.error('Error fetching progress:', error);
                clearInterval(pollingInterval); // Optionally clear interval on error
                setIsComputing(false); // Set isComputing to false when the task is done

            });
    };


    useEffect(() => {
        if (!sessionToken) {
            // Alert the user and navigate to /start immediately
            alert("Session token is missing. Please upload an event log first.");
            navigate("/start");
        }
        else {
            console.log("Session token found:", sessionToken)
        }


    }, [sessionToken, navigate]);
    const [sliderValues, setSliderValues] = useState(Array(measures.length).fill(0));


    useEffect(() => {
        return () => {
            if (pollingInterval) {
                clearInterval(pollingInterval);
            }
        };
    }, []);

    const handleSliderChange = (index, value) => {
        // Update the slider values in the state
        const updatedValues = [...sliderValues];
        updatedValues[index] = value;
        setSliderValues(updatedValues);
    };

    const handleButtonClick = () => {
        setIsComputing(true);
        const requestData = {
            sliderValues,
            sessionToken,
        };
        startPolling(); // Start polling for progress updates

        console.log({ sliderValues })
        // Send the slider values to the backend
        axios.post("https://proreco.co:8000/api/submitWeights", { requestData })
            .then((response) => {

                console.log('Successfully sent weights:');
                console.log("this is what we got back, it should be a recommendation: ", response.data)
                const relevantMeasures = measures.filter((measure, index) => sliderValues[index] > 0);
                console.log("relevantMeasuresd")
                console.log(relevantMeasures)
                // Encode the filteredSliderValues object and other data into the URL
                const urlParams = {
                    recommendation: encodeURIComponent(JSON.stringify(response.data.predictonDict)),
                    sessionToken: encodeURIComponent(sessionToken),
                    algoMeasureDict: encodeURIComponent(JSON.stringify(response.data.algoMeasureDict)),
                    // Add the filteredSliderValues to the URL
                    relevantMeasures: encodeURIComponent(JSON.stringify(relevantMeasures)),
                };
                const queryParams = Object.keys(urlParams).map(key => `${key}=${urlParams[key]}`).join('&');
                const finalUrl = `/recommend?${queryParams}`;
                const imageUrl = "https://proreco.co/cuteIcon.png"
                Swal.fire({
                    title: 'Success ! Recommendations Incoming.',
                    confirmButtonColor: '#BF3604',
                    imageUrl: imageUrl,
                    imageWidth: 250,
                    imageHeight: 250,
                    imageAlt: 'Custom image',
                    animation: true

                }).then(() => {
                    // This code will execute after Swal alert is closed

                    navigate(finalUrl)

                });
            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
                setIsComputing(false); // Set isComputing to false after receiving the data

            });

    };

    const mainDivStyle = {
        display: 'flex',                 // Equivalent to 'flex'
        flexDirection: 'column',        // Equivalent to 'flex-col'
        alignItems: 'center',           // Equivalent to 'items-center'
        justifyContent: 'center',       // Equivalent to 'justify-center'

    };
    const buttonStyle = {
        display: 'flex',        // Equivalent to 'flex'
        width: '100%',          // Equivalent to 'w-full'
        justifyContent: 'center',
        marginBottom: "15vh"
    };
    const rankSliderConatinerStyle = {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginBottom: "8vh"
    }



    return (
        <ChooseLayout>
            <div style={{ mainDivStyle }}>
                {isComputing && (
                    <div style={overlayStyle}>
                        <div style={{ ...progressWheelStyle, marginRight: "12vw" }}>
                            <ProgressWheel percentage={parsePercentage} text="Parsing" />
                        </div>
                        <div style={{ ...progressWheelStyle, marginRight: "12vw" }}>
                            <ProgressWheel percentage={featurePercentage} text={featureName} />
                        </div>
                        <div style={progressWheelStyle}>
                            <ProgressWheel percentage={predictPecentage} text="Predicting" />
                        </div>
                    </div>
                )}




                {!isComputing &&
                    (


                        <div style={rankSliderConatinerStyle}>
                            {measures.map((measure, index) => (
                                <div key={index} style={{
                                    marginBottom: "6vh", width: "90vw"
                                }}>
                                    <LabeledSlider
                                        value={sliderValues[index]}
                                        onChange={(value) => handleSliderChange(index, value)}
                                        label={measure}
                                    />
                                </div>
                            ))}


                        </div>
                    )}

                {!isComputing &&
                    (<div style={buttonStyle}>
                        <RedirectButton text="Get Recommendations !" onClick={handleButtonClick} />
                    </div>

                    )}

                {isComputing &&
                    <div style={{
                        marginBottom: "70vh"
                    }} />}
            </div>
        </ChooseLayout >
    )
}

export default RankingPage
