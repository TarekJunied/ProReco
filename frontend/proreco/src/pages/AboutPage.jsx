import ChooseLayout from "../layout/ChooseLayout";
import InfoBox from "../components/InfoBox"
import texts from "../constants/texts";
const AboutPage = () => {

    return (
        <ChooseLayout>

            <InfoBox title="AI generated, will be removed soon">
                {texts.about}
            </InfoBox>

        </ChooseLayout>

    );

}
export default AboutPage;