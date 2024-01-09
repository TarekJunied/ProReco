import { useState, useRef, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import RedirectButton from './RedirectButton';
import NextFeature from './NextFeature';





function formatText(s) {
    // Replace all underscores with spaces
    return s
        .replace(/_/g, ' ')
        // Split the string into an array of words, then map each one
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

const textStyle = {
    color: "white",
    textAlign: "center",
    fontSize: "30px",
    marginTop: "2vh"

}

const resultStyle = {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: "3vh"
}



const ShapPlot = ({ labels, featureNames, plotValues, featureValues, predictedValue }) => {


    const maxPlotValue = Math.abs(plotValues[0] - Math.max(...plotValues))
    const minPlotValue = Math.abs(plotValues[0] - Math.min(...plotValues))
    const offset = Math.max(maxPlotValue, minPlotValue)

    const maxVal = plotValues[0] + offset
    const minVal = plotValues[0] - offset


    const chartRef = useRef(null);
    const chartInstanceRef = useRef(null); // Ref for the Chart.js instance
    const [caption, setCaption] = useState(""); // Initialize caption state
    const [index, setIndex] = useState(0); // To track which data point to add next
    const [currentFeature, setCurrentFeature] = useState("Click the button above to check the impact of the features")

    useEffect(() => {


        if (chartRef.current) {
            const ctx = chartRef.current.getContext('2d');
            let myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: "SHAP Value",
                        borderWidth: 2,
                        borderColor: "rgba(75,192,192,1)",
                        pointBackgroundColor: "red",
                        pointBorderColor: "red",
                    }]
                },
                options: {
                    indexAxis: 'y',
                    scales: {
                        x: {
                            min: minVal,
                            max: maxVal,
                            title: {
                                display: true,
                                text: 'Impact on Measure'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Features'
                            }
                        }
                    }
                }
            });

            chartInstanceRef.current = myChart; // Assign the chart instance to its ref

            return () => {
                myChart.destroy(); // Ensure to destroy the chart instance on cleanup
            };
        }
    }, []); // Dependency array is empty, so this effect runs once after initial render




    const addData = () => {
        const myChart = chartInstanceRef.current; // Access the chart instance

        if (index < plotValues.length) {
            myChart.data.datasets[0].data[plotValues.length - index - 1] = plotValues[index];
            console.log(index);

            let isIncrease = plotValues[index] - plotValues[index - 1] > 0
            let arrowEmoji = isIncrease ? "🟢⬆️" : "🔴⬇️"
            setCaption(
                index > 0
                    ? `${arrowEmoji}  ${Math.abs(plotValues[index] - plotValues[index - 1]).toFixed(3)}`
                    : `Initial value before influence of features ${plotValues[0].toFixed(3)}`
            );


            if (featureNames.length - index - 1 >= 0) {
                setCurrentFeature(formatText(featureNames[featureNames.length - index - 1]))
                setIndex((prevIndex) => prevIndex + 1); // Update the index

            }


            myChart.update();



        }
        else {


            setCaption("")
            setIndex(0)
            setCurrentFeature("Click the button above to check the impact of the features")
            myChart.data.datasets.forEach((dataset) => {
                dataset.data = []; // Reset data array
            });
            myChart.update();


        }

    };





    return (
        <div style={{ width: "100%" }}>
            <div style={{ backgroundColor: 'white' }}> {/* Set background color here */}
                <canvas ref={chartRef} />
            </div>
            <div style={{ width: "20vw", marginTop: "4vh" }}>
                <NextFeature onClick={addData} text={featureNames.length - index - 1 >= 0 ? "Next Feature" : "Reset"} />
            </div>
            <div style={resultStyle}>

                <div style={textStyle}>
                    {currentFeature}
                </div>
                <div style={textStyle}>{caption}</div>
            </div>

        </div>

    );
};

export default ShapPlot;
