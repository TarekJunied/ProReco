import { useEffect, useRef } from 'react';
import * as joint from 'jointjs';
import 'jointjs/dist/joint.css'; // Import JointJS styles

const PetriNet = ({ windowWidthInVW, data }) => {
    const ref = useRef(null); // Create a reference to the DOM element


    useEffect(() => {
        if (ref.current && data && data.places && data.transitions && data.links) {

            const paperWidth = windowWidthInVW * window.innerWidth
            const paperHeight = paperWidth / data.width_to_height_ratio


            const graph = new joint.dia.Graph();
            const paper = new joint.dia.Paper({
                el: ref.current,
                linkPinning: false,                             // prevent dangling links
                model: graph,
                defaultAnchor: { name: 'perpendicular' },
                defaultConnectionPoint: { name: 'boundary' },
                width: paperWidth,
                height: paperHeight,
                gridSize: 10,
                background: {
                    color: "transparent",

                },



                /*,
                interactive: function (cellView, method) {
                    return cellView instanceof joint.dia.ElementView; // Only allow interaction with joint.dia.LinkView instances.
                }*/

            });


            // Create places
            const places = data.places.map(place => new joint.shapes.pn.Place({

                position: { x: place.x * paperWidth, y: place.y * paperHeight },
                attrs: { circle: { fill: 'white' } },
                tokens: place.tokens || 0,
                id: place.id,
            }));

            const transitions = data.transitions.map(transition => new joint.shapes.pn.Transition({
                position: { x: transition.x * paperWidth, y: transition.y * paperHeight },
                attrs: {
                    rect: { fill: 'black' },
                    text: {
                        text: transition.label, // Replace with your desired label text
                        fill: 'white',      // Customize label text color
                        'font-size': 14,    // Customize label font size
                    },
                },
                id: transition.id,
            }));
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
                        '.connection': { stroke: 'black' },

                    },
                });
                paper.findViewByModel(curLink)

                return curLink
            }).filter(link => link !== null); // Filter out inva
            graph.addCells(links)
            links.forEach((link) => { paper.findViewByModel(link).options.interactive = false })
            //paper.$el.css('pointer-events', 'none');
        }
    }, [data, windowWidthInVW]);


    if (!data || !data.places || !data.transitions || !data.links) {
        // Add your error handling logic here, e.g., display an error message
        console.log(JSON.stringify(data))
        return <div>Error: Data is missing or invalid.</div>;
    }

    return <div ref={ref} style={{ border: '2px solid black' }}></div>;
};

export default PetriNet;
