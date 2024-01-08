import InfoLayout from "../layout/InfoLayout"
import InfoBox from "../components/InfoBox"
import texts from "../constants/texts";
const AboutPage = () => {

    return (
        <InfoLayout>

            <InfoBox title="AI generated, will be removed soon">
                {texts.about}
            </InfoBox>

        </InfoLayout>

    );

}
export default AboutPage;