import { useEffect, useRef } from 'react';
import * as joint from 'jointjs';
import 'jointjs/dist/joint.css'; // Import JointJS styles
const V = joint.V;
const namespace = joint.shapes;

function fireTransition(paper, graph, t, sec) {

    var inbound = graph.getConnectedLinks(t, { inbound: true });
    var outbound = graph.getConnectedLinks(t, { outbound: true });

    var placesBefore = inbound.map(function (link) {
        return link.getSourceElement();
    });
    var placesAfter = outbound.map(function (link) {
        return link.getTargetElement();
    });

    var isFirable = true;
    placesBefore.forEach(function (p) {
        if (p.get('tokens') <= 0) {
            isFirable = false;
        }
    });

    if (isFirable) {

        placesBefore.forEach(function (p) {
            // Let the execution finish before adjusting the value of tokens. So that we can loop over all transitions
            // and call fireTransition() on the original number of tokens.
            setTimeout(function () {
                if (p.get('tokens') <= 1) {
                    p.set('tokens', 0)
                }
                else {
                    p.set('tokens', p.get('tokens') - 1);

                }

            }, 0);

            var links = inbound.filter(function (l) {
                return l.getSourceElement() === p;
            });

            links.forEach(function (l) {
                var token = V('circle', { r: tokenRadius, fill: tokenColor });
                l.findView(paper).sendToken(token, sec * 1000);
            });
        });

        placesAfter.forEach(function (p) {

            var links = outbound.filter(function (l) {
                return l.getTargetElement() === p;
            });

            links.forEach(function (l) {
                var token = V('circle', { r: tokenRadius, fill: tokenColor });
                l.findView(paper).sendToken(token, sec * 1000, function () {
                    p.set('tokens', p.get('tokens') + 1)
                });
            });
        });
    }
}



function simulate(transitions, places, paper, graph, sec) {

    transitions.forEach(function (t) {
        fireTransition(paper, graph, t, sec);
    });



    return setInterval(function () {

        transitions.forEach(function (t) {
            fireTransition(paper, graph, t, sec);
        });
    }, 3000);
}


function stopSimulation(simulationId) {
    clearInterval(simulationId);
}





function createTransitionObject(transition, paperWidth, paperHeight, widthScalingFactor, heightScalingFactor) {
    // Determine fill color based on the transition.label, or set a default
    let fill = transition.label === '\\N' ? 'black' : 'white'; // Example condition or implement your own logic

    return {
        position: {
            x: (transition.x * paperWidth) / widthScalingFactor,
            y: (transition.y * paperHeight) / heightScalingFactor
        },
        size: { width: 40, height: 40 },
        attrs: {
            '.root': {
                'stroke': transitionStrokeColor,
            },
            rect: {
                fill: fill, // Set the fill color
            },
            text: {
                text: transition.label, // Use transition.label
                fill: 'black',          // Customize label text color
                'font-size': 15,
                'ref-x': 0.5,           // center the text in the x-axis inside the rectangle
                'ref-y': 0.5,           // center the text in the y-axis inside the rectangle
                'text-anchor': 'middle', // ensures the text is centered
                'y-alignment': 'middle', // vertically centers the text
            }
        },
        id: transition.id, // Place the id outside of attrs
    };
}



function createPlaceObject(place, paperWidth, paperHeight, widthScalingFactor, heightScalingFactor) {
    // Determine if the place is the "end" place
    let addition = 0
    let strokeWidth = 3
    let strokeColor = "#000000"
    if (place.label === "start") {
        addition = 1
        strokeColor = "#FF0000"
    }
    if (place.label == "end") {
        strokeColor = "blue"
    }
    return {
        position: {
            x: (place.x * paperWidth) / widthScalingFactor,
            y: (place.y * paperHeight) / heightScalingFactor
        },
        attrs: {
            '.root': {
                'stroke': placeStrokeColor,
                'stroke-width': strokeWidth
            },
            '.tokens > circle': {
                'fill': tokenColor,
                'r': tokenRadius
            },
        },

        tokens: addition,
        id: place.id,
    };
}


const widthScalingFactor = 1.2
const heightScalingFactor = 1.2
const tokenColor = "#FF4F00"
const placeStrokeColor = "#BF3604"
const transitionStrokeColor = "red"
const tokenRadius = 7
const PetriNet = ({ data, paperWidthInPX }) => {
    const ref = useRef(null); // Create a reference to the DOM element


    useEffect(() => {
        if (ref.current && data && data.places && data.transitions && data.links) {

            const paperWidth = paperWidthInPX
            const paperHeight = (data.total_height / data.total_width) * paperWidth


            const graph = new joint.dia.Graph();
            const paper = new joint.dia.Paper({
                el: ref.current,
                linkPinning: false,                             // prevent dangling links
                model: graph,
                defaultAnchor: { name: 'perpendicular' },
                defaultConnectionPoint: { name: 'boundary' },
                width: paperWidth,
                height: paperHeight,
                gridSize: 1,
                background: {
                    color: "white",

                },
                cellViewNamespace: namespace

            });


            const places = data.places.map(place =>
                new joint.shapes.pn.Place(createPlaceObject(place, paperWidth, paperHeight, widthScalingFactor, heightScalingFactor))
            );

            const transitions = data.transitions.map(transition =>
                new joint.shapes.pn.Transition(createTransitionObject(transition, paperWidth, paperHeight, widthScalingFactor, heightScalingFactor))
            );

            graph.addCells([...places, ...transitions]);


            const links = data.links.map(link => {
                const sourceElement = graph.getCell(link.sourceid.toString());
                const targetElement = graph.getCell(link.targetid.toString());

                if (!sourceElement || !targetElement) {
                    console.warn(`Invalid source or target ID in link: ${link.sourceid} -> ${link.targetid}`);
                    return null; // Skip invalid links
                }
                let curLink = new joint.shapes.pn.Link({
                    source: { id: sourceElement.id },
                    target: { id: targetElement.id },
                    attrs: {
                        '.connection': {
                            'fill': 'none',
                            'stroke-linejoin': 'round',
                            'stroke-width': '1.2',
                            'stroke': '#4b4a67'
                        }
                    },
                });
                //curLink.router("manhattan");

                curLink.connector("smooth")

                graph.addCell(curLink)
                var cell = paper.findViewByModel(graph.getLastCell())
                cell.model.attr('./pointer-events', 'none')

                return curLink
            }).filter(link => link !== null); // Filter out inva
            //graph.addCells(links)
            links.forEach((link) => { paper.findViewByModel(link).options.interactive = false })
            //paper.$el.css('pointer-events', 'none');



            simulate(transitions, places, paper, graph, 1)


        }
    }, [data, paperWidthInPX]);


    if (!data || !data.places || !data.transitions || !data.links) {
        // Add your error handling logic here, e.g., display an error message
        console.log(JSON.stringify(data))
        return <div>Error: Data is missing or invalid.</div>;
    }

    return <div ref={ref} style={{ border: '2px solid black' }}></div>;
};

export default PetriNet;
