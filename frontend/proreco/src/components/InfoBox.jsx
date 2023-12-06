import styles from '../styles';
import "./styles/InfoBox.css";

// eslint-disable-next-line react/prop-types
const InfoBox = ({ children, title }) => {
    return (
        <div className="pt-2 pb-4 ">
            <div className={`text-left ml-52 ${styles.infoboxTitle} `}>
                {title}
            </div>
            <div className="flex flex-col items-center relative padding pb-6">

                <div style={{
                    width: '75vw',
                    border: '1px solid #ccc',
                    padding: '20px',
                    background: 'rgba(255, 165, 0, 0.2)',
                    color: 'white',
                    fontFamily: 'YourFontFamily, sans-serif',
                }}>
                    <p className={`leading-relaxed ${styles.infobox}`}>
                        {children}
                    </p>
                </div>
            </div>
        </div>
    );
}

export default InfoBox;
