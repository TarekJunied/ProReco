import ChooseLayout from "../layout/ChooseLayout";
import { AlgorithmPortfolio } from "../constants";

const RecommendPage = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const recommendationParam = urlParams.get('recommendation');
    const recommendationData = JSON.parse(decodeURIComponent(recommendationParam));

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
            </div>

        </ChooseLayout >
    );
};

export default RecommendPage;
