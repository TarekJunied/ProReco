// eslint-disable-next-line react/prop-types
const StartButton = ({ text, styles, onClick }) => {
    return (
        <button
            type="button"
            style={{
                width: "800px", // Set a fixed width
                height: "auto", // Let the height adjust automatically
            }}
            className={`py-2 px-40 font-bold text-[25px] rounded-[8px] text-primary outline-none ${styles} text-white text-center`}
            onClick={onClick} // Add the onClick handler here
        >
            {text}
        </button>
    )
}

export default StartButton;
