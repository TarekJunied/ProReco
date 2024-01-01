/* eslint-disable */




const Button = ({ text, style, onClick }) => {
    return (

        <button type="button" style={style} onClick={onClick}>
            {text}
        </button>
    )
}

export default Button
