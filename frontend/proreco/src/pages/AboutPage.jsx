import InfoLayout from "../layout/InfoLayout"
import InfoBox from "../components/InfoBox"
import texts from "../constants/texts";
const AboutPage = () => {

    return (
        <InfoLayout>
            <InfoBox title="About Process Mining">
                {"who actually cares about process mining, let's discuss something more relevant"}

            </InfoBox>
            <InfoBox title="TAREK IS THE BEST">
                {texts.tarekText}
            </InfoBox>

        </InfoLayout>

    );

}
export default AboutPage;