import ChooseLayout from "../layout/ChooseLayout"
import { useLocation } from 'react-router-dom';

const RecommendPage = () => {


    const location = useLocation();
    const params = new URLSearchParams(location.search);
    const recommendation = params.get('recommendation');

    return (
        <ChooseLayout>
            <div className="flex-row justify-center p-0">
                <div className="flex justify-center w-screen mt-10">
                    {recommendation}
                </div>
            </div>
        </ChooseLayout>
    )
}

export default RecommendPage
