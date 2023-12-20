import fs from 'fs/promises';
import xml2js from 'xml2js';
const parser = new xml2js.Parser();

async function parsePNMLFile(filePath) {
    try {
        const data = await fs.readFile(filePath, "utf8");
        parser.parseString(data, (err, result) => {
            if (err) {
                console.error('Error parsing XML:', err);
                return;
            }


            console.log(result.pnml.net[0])



            const places = result.pnml.net[0].place || [];
            const transitions = result.pnml.net[0].transition || [];
            const edges = result.pnml.net[0].arc || [];

            console.log('Places:', places.map(place => place.$.id));
            console.log('Transitions:', transitions.map(transition => transition.$.id));
            console.log('Edges:', edges.map(edge => ({ source: edge.$.source, target: edge.$.target })));
        });
    } catch (err) {
        console.error('Error reading file:', err);
    }
}

const filePath = process.argv[2]; // Get file path from command line arguments
parsePNMLFile(filePath);
