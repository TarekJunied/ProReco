import ChooseLayout from "../layout/ChooseLayout";
import { AlgorithmPortfolio } from "../constants";
import StartButton from "../components/StartButton"
import { useNavigate } from 'react-router-dom';

const RecommendPage = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const recommendationParam = urlParams.get('recommendation');
    const sessionTokenParam = urlParams.get('sessionToken');

    const recommendationData = JSON.parse(decodeURIComponent(recommendationParam));
    const sessionToken = decodeURIComponent(sessionTokenParam)

    const navigate = useNavigate();


    const handleMineButtonClick = () => {

        console.log("don't click me bitch")

        navigate(`/mine?sessionToken=${sessionToken}`);
        /*
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
            */
    };


    const handleMainMenuButtonClick = () => {

        console.log("don't click me bitch")

        /*
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
            */
    };





    return (
        <ChooseLayout>
            <div className="flex-row justify-center p-0">
                <div className="flex justify-center w-screen mt-10">
                    <div className="flex-col">
                        {AlgorithmPortfolio.map((DiscoveryAlgorithm, index) => (
                            <div key={index} className="text-center text-bold text-white text-[30px] flex-row flex  justify-center mb-10">
                                <div className="uppercase">{DiscoveryAlgorithm}:</div>

                            </div>
                        ))}
                    </div>
                    <div className="flex-col" style={{ width: 300 }}>
                        {AlgorithmPortfolio.map((DiscoveryAlgorithm, index) => (
                            <div key={index} className="text-center text-bold text-white text-[30px] flex-row flex  justify-center mb-10">
                                <div>{recommendationData[DiscoveryAlgorithm]}</div>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="flex flex-col items-center justify-center flex-grow mb-40">
                    <div className="flex flex-col items-center space-y-20 flex-grow">
                        <div className="flex-grow"></div>
                        <div className="w-full">
                            <StartButton
                                text="Mine a process model"
                                styles="bg-orange-gradient text-[40px]"
                                onClick={handleMineButtonClick}
                            />
                        </div>
                        <div className="flex-grow"></div>
                        <div className="w-full">
                            <StartButton
                                text="Back to main menu"
                                styles="bg-orange-gradient text-[40px]"
                                onClick={handleMainMenuButtonClick}
                            />
                        </div>

                    </div>
                </div>
            </div>

        </ChooseLayout >
    );
};

export default RecommendPage;
