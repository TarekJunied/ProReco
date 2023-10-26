import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios"
import ChooseLayout from "../layout/ChooseLayout"
import RankSlider from "../components/RankSlider"
import StartButton from "../components/StartButton"
import { measures } from "../constants"

const RankingPage = () => {
    const navigate = useNavigate();
    const [sliderValues, setSliderValues] = useState(Array(measures.length).fill(0));

    const handleSliderChange = (index, value) => {
        // Update the slider values in the state
        const updatedValues = [...sliderValues];
        updatedValues[index] = value;
        setSliderValues(updatedValues);
    };

    const handleButtonClick = () => {
        console.log({ sliderValues })
        // Send the slider values to the backend
        axios.post("http://localhost:8000/api/submitWeights", { sliderValues })
            .then((response) => {
                // Assuming a successful response from the backend
                console.log("Data sent to the backend:", response.data);

                // Navigate to the next page
                navigate("/loading");
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
