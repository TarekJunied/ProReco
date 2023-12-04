
import "./styles/InfoBox.css"
// eslint-disable-next-line react/prop-types
const InfoBox = ({ children }) => {
    return (
        <div className="infobox">
            {children}
        </div>
    )
}

export default InfoBox
