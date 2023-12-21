import React, { useEffect, useRef } from 'react';
import * as joint from 'jointjs';
import 'jointjs/dist/joint.css'; // Import JointJS styles

// eslint-disable-next-line react/prop-types
const PetriNet = ({ paperWidth, paperHeight, data }) => {
    const ref = useRef(null); // Create a reference to the DOM element
    // REMEMBER TO MAKE SILENT TRANSITIONS , I.E: transitions with labels '\\N' black
    // don't use label attribute for places, but use label attribute for transitions




    useEffect(() => {
        if (ref.current && data.places && data.transitions && data.links) {
            const graph = new joint.dia.Graph();
            const paper = new joint.dia.Paper({
                el: ref.current,
                model: graph,
                width: paperWidth,
                height: paperHeight,
                gridSize: 1
            });

            // Create places
            const places = data.places.map(place => new joint.shapes.pn.Place({
                position: { x: place.x * paperWidth, y: place.y * paperHeight },
                attrs: { circle: { fill: 'red' } },
                id: place.id,
            }));

            // Create transitions
            const transitions = data.transitions.map(transition => new joint.shapes.pn.Transition({
                position: { x: transition.x * paperWidth, y: transition.y * paperHeight },
                attrs: { rect: { fill: 'black' } },
                id: transition.id,
            }));

            // Create links
            const links = data.links.map(link => new joint.shapes.pn.Link({
                source: { id: link.sourceid },
                target: { id: link.targetid },
                attrs: { '.connection': { stroke: 'black' } }
            }));

            // Add all elements to the graph
            graph.addCells([...places, ...transitions, ...links]);
        }
    }, [data, paperWidth, paperHeight]);

    return <div ref={ref} style={{ border: '2px solid black' }}></div>;
};

export default PetriNet;
