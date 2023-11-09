import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"
import ChooseLayout from "../layout/ChooseLayout"
import RankSlider from "../components/RankSlider"
import StartButton from "../components/StartButton"
import { measures } from "../constants"


const RankingPage = () => {
    const sessionToken = localStorage.getItem('sessionToken');



    const navigate = useNavigate();

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

    const handleSliderChange = (index, value) => {
        // Update the slider values in the state
        const updatedValues = [...sliderValues];
        updatedValues[index] = value;
        setSliderValues(updatedValues);
    };

    const handleButtonClick = () => {

        const requestData = {
            sliderValues,
            sessionToken,
        };




        console.log({ sliderValues })
        // Send the slider values to the backend
        axios.post("http://localhost:8000/api/submitWeights", { requestData })
            .then((response) => {

                console.log('Successfully sent weights:');
                console.log("this is what we got back, it should be a recommendation: ", response.data)

                // maybe clean the data
                navigate(`/recommend?recommendation=${encodeURIComponent(JSON.stringify(response.data))}`);
            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
            });
    };








    return (
        <ChooseLayout>
            <div className="flex-row justify-center p-0">
                <div className="flex justify-center w-screen mt-10">
                    <div className="flex flex-col">
                        {measures.map((measure, index) => (
                            <label key={index} className="text-[40px] mb-4" style={{ color: "#F25C05" }}>{measure}</label>
                        ))}
                    </div>
                    <div className="flex-col" style={{ width: 800 }}>
                        {measures.map((measure, index) => (
                            <RankSlider key={index}
                                value={sliderValues[index]}
                                onChange={(value) => handleSliderChange(index, value)} />
                        ))}
                    </div>
                </div>
                <div className="flex justify-center mt-10 mb-40"> {/* Add this container div */}
                    <StartButton text="Get Recommendations !" styles="bg-orange-gradient text-[40px]" onClick={handleButtonClick} />
                </div>
            </div>
        </ChooseLayout>
    )
}

export default RankingPage
