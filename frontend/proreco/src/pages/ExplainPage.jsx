import { useState, useEffect } from 'react'
import ChooseLayout from '../layout/ChooseLayout'
import InfoBox from '../components/InfoBox'
import { AlgorithmPortfolio } from '../constants'
import { measures } from '../constants'
import ShapPlot from '../components/ShapPlot'
import RedirectButton from '../components/RedirectButton'
import VisibilityButton from '../components/VisiblityButton'
import NextFeature from '../components/NextFeature'
import axios from 'axios'; // You can use Axios for making HTTP requests
import Swal from 'sweetalert2';
import LoadingSpinner from '../components/LoadingSpinner'

const plotValues = [0.7409909948064592, 0.746806967686832, 0.752748746107448, 0.7463866110304889, 0.7537428794781524, 0.762164312723242, 0.7718393193463003, 0.7827698977626607, 0.7943310253072154, 0.8099993363801724, 0.9721512660592142]
const featureNames = ['length_one_loops', 'avg_event_repetition_intra_trace', 'percentage_concurrency', 'dfg_variation_coefficient_variable_degree', 'spatial_proximity_connectedness', 'average_number_of_self_loops_per_trace', 'number_of_arcs', 'dfg_wcc_variation_coefficient', 'maximum_node_degree', 'activities_max']
const featureValues = [0.2, 1.3819849874895747, 0.06, 0.7483314773547882, 0.5555555555555556, 0.003336113427856547, 15.0, 2.7619423815302104, 11.0, 2324.0]
const predictedValue = 0.71
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

const translateMeasureIntoPythonSyntax = (jsMeasure) => {
    // Make the string lowercase
    const lowercaseMeasure = jsMeasure.toLowerCase();

    // Replace spaces with underscores
    const pythonSyntaxMeasure = lowercaseMeasure.replace(/ /g, '_');

    return pythonSyntaxMeasure;
};

function formatText(s) {
    // Replace all underscores with spaces
    return s
        .replace(/_/g, ' ')
        // Split the string into an array of words, then map each one
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}





const ExplainPage = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const [isVisible, setIsVisible] = useState({});
    const [isComputing, setIsComputing] = useState(true)
    const [algoDiscValues, setAlgoDiscoValues] = useState(null)
    const sessionTokenParam = urlParams.get('sessionToken');
    const sessionToken = decodeURIComponent(sessionTokenParam)

    function getLabels(discoveryAlgorithm, measure) {
        let key = discoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoDiscValues[key].labels
    }
    function getFeatureNames(discoveryAlgorithm, measure) {
        let key = discoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoDiscValues[key].top_features
    }
    function getFeatureValues(discoveryAlgorithm, measure) {
        let key = discoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoDiscValues[key].feature_values
    }
    function getPlotValues(discoveryAlgorithm, measure) {
        let key = discoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoDiscValues[key].plot_values
    }
    function getPredictedValue(discoveryAlgorithm, measure) {
        let key = discoveryAlgorithm + "-" + translateMeasureIntoPythonSyntax(measure)
        return algoDiscValues[key].predictedValue
    }


    useEffect(() => {
        const requestData = {
            sessionToken
        };
        axios.post(`${import.meta.env.VITE_API_URL}/api/getExplainationDict`, { requestData })
            .then((response) => {
                const imageUrl = "https://proreco.co/cuteIcon.png"
                Swal.fire({
                    title: 'Success ! Explainations Incoming.',
                    confirmButtonColor: '#BF3604',
                    imageUrl: imageUrl,
                    imageWidth: 250,
                    imageHeight: 250,
                    imageAlt: 'Custom image',
                    animation: true

                })
                console.log(response)
                console.log(response.data)
                setAlgoDiscoValues(response.data)
                setIsComputing(false)

            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
            });
    }, []); // The empty dependency array [] means this effect will run once after the initial render








    const toggleVisibility = (discoveryAlgorithm, measureName) => {
        // Update the visibility state
        setIsVisible(prevState => ({
            ...prevState,
            [discoveryAlgorithm]: {
                ...prevState[discoveryAlgorithm],
                [measureName]: !prevState[discoveryAlgorithm]?.[measureName]
            }
        }));
    };






    return (
        <ChooseLayout>

            {isComputing && (

                <div style={overlayStyle}>

                    <LoadingSpinner text={"Explaining"} />

                </div>
            )
            }
            {isComputing &&
                <div style={{
                    marginBottom: "70vh"
                }} />}







            {AlgorithmPortfolio.map((discoveryAlgorithm, index) => (
                <div key={index} style={{ width: "100%" }}>
                    <InfoBox title={formatText(discoveryAlgorithm)} style={{ width: '100%' }}>
                        {measures.map((measure, measureIndex) => {
                            const isPlotVisible =
                                isVisible[discoveryAlgorithm]?.[measure] || false;
                            return (
                                <div
                                    key={measureIndex}
                                    style={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        justifyContent: 'center',
                                        alignItems: 'center',
                                        marginBottom: '6vh',
                                        width: '100%' // Ensure this div takes full width

                                    }}
                                >
                                    <VisibilityButton
                                        text={isPlotVisible ? "Hide Explaination" : formatText(measure)}
                                        onClick={() => toggleVisibility(discoveryAlgorithm, measure)}
                                    />

                                    {isPlotVisible && (
                                        <div
                                            style={{
                                                display: 'flex',
                                                justifyContent: 'center',
                                                width: '100%',
                                                marginTop: '2vh',
                                            }}
                                        >
                                            <ShapPlot
                                                labels={getLabels(discoveryAlgorithm, measure)}
                                                featureNames={getFeatureNames(discoveryAlgorithm, measure)}
                                                featureValues={getFeatureValues(discoveryAlgorithm, measure)}
                                                plotValues={getPlotValues(discoveryAlgorithm, measure)}
                                                predictedValue={getPredictedValue(discoveryAlgorithm, measure)}
                                            />
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </InfoBox>
                </div>
            ))}
        </ChooseLayout>
    );
};

export default ExplainPage;
