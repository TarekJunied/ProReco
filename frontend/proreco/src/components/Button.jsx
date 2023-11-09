/* eslint-disable */

const Button = ({ text, styles, onClick }) => {
    return (

        <button type="button" className={`py-4 px-6 font-bold text-[25px] rounded-[8px] text-primary outline-none ${styles} text-white`} onClick={onClick}>
            {text}
        </button>
    )
}

export default Button
