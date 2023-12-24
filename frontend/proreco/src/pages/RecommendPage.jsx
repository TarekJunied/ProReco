import ChooseLayout from "../layout/ChooseLayout";
import { AlgorithmPortfolio, measures } from "../constants";
import StartButton from "../components/StartButton"
import { useNavigate } from 'react-router-dom';
import AlgorithmScore from "../components/AlgorithmScore";
import { Tooltip } from 'react-tooltip'
const translateMeasureIntoPythonSyntax = (jsMeasure) => {
    // Make the string lowercase
    const lowercaseMeasure = jsMeasure.toLowerCase();

    // Replace spaces with underscores
    const pythonSyntaxMeasure = lowercaseMeasure.replace(/ /g, '_');

    return pythonSyntaxMeasure;
};



const RecommendPage = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const recommendationParam = urlParams.get('recommendation');
    const algoMeasureDictParam = urlParams.get('algoMeasureDict')
    const relevantMeasuresParam = urlParams.get('relevantMeasures')
    const sessionTokenParam = urlParams.get('sessionToken');

    const recommendationData = JSON.parse(decodeURIComponent(recommendationParam));
    const algoMeasureDict = JSON.parse(decodeURIComponent(algoMeasureDictParam));
    const sessionToken = decodeURIComponent(sessionTokenParam)
    const relevantMeasures = JSON.parse(decodeURIComponent(relevantMeasuresParam));



    const getPredictedMeasureValue = (DiscoveryAlgorithm, measure) => {
        let key = DiscoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoMeasureDict[key]
    }


    const navigate = useNavigate();


    const handleMineButtonClick = () => {


        navigate(`/mine?sessionToken=${sessionToken}`);

    };


    const handleMainMenuButtonClick = () => {
        navigate("/start")
    };

    AlgorithmPortfolio.sort((a, b) => {
        // Assuming recommendationData[DiscoveryAlgorithm] holds a sortable value.
        // Adjust the comparison for the specific data type and desired order.
        return recommendationData[b] - recommendationData[a]; // For descending order
        // Use recommendationData[a] - recommendationData[b] for ascending order
    });

    const headingStyle = {

        alignSelf: "center",
        color: "white",
        fontSize: "5vw"

    }

    const toolTipStyle = {
        fontSize: "2vw"
    }
    const tooltipTexts = {};

    AlgorithmPortfolio.forEach(DiscoveryAlgorithm => {
        tooltipTexts[DiscoveryAlgorithm] = `Predicted Values:<br/>${relevantMeasures.map(measure => `${measure}:${getPredictedMeasureValue(DiscoveryAlgorithm, measure)}<br/>`).join('')}`
    });



    return (
        <ChooseLayout>
            <h1 style={headingStyle}>Leaderboard  🏆</h1>


            <div className="flex justify-center w-screen mt-10">
                <div className="flex-row">
                    {AlgorithmPortfolio.map((DiscoveryAlgorithm, index) => (
                        <div key={index} style={{
                            marginTop: index === 0 ? "0" : "5vh",
                            width: "50vw" // add top margin for all but the first item
                        }}>
                            <a
                                data-tooltip-id={`${DiscoveryAlgorithm}sToolTip`}
                                data-tooltip-html={tooltipTexts[DiscoveryAlgorithm]}
                                data-tooltip-place="right"

                            >
                                <AlgorithmScore
                                    placement={index + 1}
                                    algorithmName={DiscoveryAlgorithm}
                                    algorithmScore={recommendationData[DiscoveryAlgorithm]}


                                />
                            </a>

                            <Tooltip id={`${DiscoveryAlgorithm}sToolTip`}
                                style={toolTipStyle}
                                place="right" />
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
                    <div className="w-full">
                        <StartButton
                            text="Back to start"
                            styles="bg-orange-gradient text-[40px]"
                            onClick={handleMainMenuButtonClick}
                        />
                    </div>

                </div>
            </div>

        </ChooseLayout >
    );
};

export default RecommendPage;
