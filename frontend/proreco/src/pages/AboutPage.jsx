import InfoLayout from "../layout/InfoLayout"
import texts from "../constants/texts"
const AboutPage = () => {

    return (
        <InfoLayout>
            <p>
                {texts.about}
            </p>
        </InfoLayout>

    );

}
export default AboutPage;