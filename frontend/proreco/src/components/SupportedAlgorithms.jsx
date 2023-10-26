
import { Link } from 'react-router-dom';
import splitLogo from '../assets/split-logo.png';
import alphaLogo from '../assets/alpha-logo.png';
import ilpLogo from '../assets/ILP-logo.png';
import heuristicLogo from '../assets/heuristic-logo.png';
import inductiveLogo from '../assets/inductive-logo.png';
import './styles/SupportedAlgorithms.css';

const SupportedAlgorithms = () => {
    // Define the URLs you want the images to link to
    const splitUrl = 'https://www.processmining.org/split';
    const alphaUrl = 'https://www.processmining.org/alpha';
    const ilpUrl = 'https://www.processmining.org/ilp';
    const heuristicUrl = 'https://www.processmining.org/heuristic';
    const inductiveUrl = 'https://www.processmining.org/inductive';

    return (
        <div className="space-y-2">
            <h1 className="text-[35px] font-bold text-white ml-56">Supported Algorithms:</h1>
            <div className="flex flex-col items-center">
                <div className="bg-orange-950 bg-opacity-30 p-4 rounded-[20px]">
                    <ul className="flex space-x-16">
                        <li>
                            <Link to={splitUrl} target="_blank" rel="noopener noreferrer">
                                <div className="flex flex-col items-center space-y-5">
                                    <img src={splitLogo} alt="Split Logo" id="split-logo" />
                                    <p className="font-normal ss:text-[xr68px] text-[25px] text-white max-w-[470px]">SPLIT</p>
                                </div>
                            </Link>
                        </li>
                        <li>
                            <Link to={alphaUrl} target="_blank" rel="noopener noreferrer">
                                <div className="flex flex-col items-center space-y-5">
                                    <img src={alphaLogo} alt="Alpha Logo" id="alpha-logo" />
                                    <p className="font-normal ss:text-[xr68px] text-[25px] text-white max-w-[470px]">ALPHA</p>
                                </div>
                            </Link>
                        </li>
                        <li>
                            <Link to={ilpUrl} target="_blank" rel="noopener noreferrer">
                                <div className="flex flex-col items-center space-y-5">
                                    <img src={ilpLogo} alt="ILP Logo" id="ILP-logo" />
                                    <p className="font-normal ss:text-[xr68px] text-[25px] text-white max-w-[470px]">ILP</p>
                                </div>
                            </Link>
                        </li>
                        <li>
                            <Link to={heuristicUrl} target="_blank" rel="noopener noreferrer">
                                <div className="flex flex-col items-center space-y-5">
                                    <img src={heuristicLogo} alt="Heuristic Logo" id="heuristic-logo" />
                                    <p className="font-normal ss:text-[xr68px] text-[25px] text-white max-w-[470px]">HEURISTIC</p>
                                </div>
                            </Link>
                        </li>
                        <li>
                            <Link to={inductiveUrl} target="_blank" rel="noopener noreferrer">
                                <div className="flex flex-col items-center space-y-5">
                                    <img src={inductiveLogo} alt="Inductive Logo" id="inductive-logo" />
                                    <p className="font-normal ss:text-[xr68px] text-[25px] text-white max-w-[470px]">INDUCTIVE</p>
                                </div>
                            </Link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default SupportedAlgorithms;
