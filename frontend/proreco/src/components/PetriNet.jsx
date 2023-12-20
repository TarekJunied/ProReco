import React, { useEffect, useRef } from 'react';
import * as joint from 'jointjs';
import 'jointjs/dist/joint.css'; // Import JointJS styles

const PetriNet = () => {
    const ref = useRef(null); // Create a reference to the DOM element

    useEffect(() => {
        if (ref.current) {
            // Create a JointJS graph and paper
            const graph = new joint.dia.Graph();
            const paper = new joint.dia.Paper({
                el: ref.current,
                model: graph,
                width: 800,
                height: 400,
                gridSize: 1
            });

            // Create Petri net elements
            // Place 1
            const place1 = new joint.shapes.pn.Place({
                position: { x: 100, y: 100 },
                attrs: { circle: { fill: 'blue' } }
            });

            // Place 2
            const place2 = new joint.shapes.pn.Place({
                position: { x: 300, y: 100 },
                attrs: { circle: { fill: 'blue' } }
            });

            // Transition
            const transition = new joint.shapes.pn.Transition({
                position: { x: 200, y: 100 },
                attrs: { rect: { fill: 'black' } }
            });

            // Links
            const link1 = new joint.shapes.pn.Link({
                source: { id: place1.id },
                target: { id: transition.id }
            });

            const link2 = new joint.shapes.pn.Link({
                source: { id: transition.id },
                target: { id: place2.id }
            });

            // Add elements to the graph
            graph.addCells([place1, place2, transition, link1, link2]);
        }
    }, []);

    return <div ref={ref} style={{ border: '2px solid black' }}></div>;
};

export default PetriNet;
