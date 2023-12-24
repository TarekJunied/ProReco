import React from 'react'
import Slider from '@mui/material/Slider';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import "../index.css"
export const themeOptions = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#FF6300',
        },
        secondary: {
            main: '#f50057',
        },
    },
});

const sliderContainerStyles = {
    width: "50vw",
    margin: '0 auto', // Center the slider container
    position: "absolute",
    right: "10%"
};

const sliderStyles = {
    height: "3.7vh",
    borderRadius: "1.5vh",
};
const labelStyle = {
    fontSize: "50px",
    color: "#FF6300"

}
const divStyle = {
    display: "flex",
    flexDirection: "row",
    alignItems: 'center',
    position: 'relative',
    justifyContent: 'space-between',// Align items vertically in the center


}

const LabeledSlider = ({ value, onChange, label }) => {

    const formatValueLabel = (value) => (
        <span style={{ fontFamily: 'outfit', fontSize: "1.3vw" }}>{value}</span>
    );

    return (
        <div style={divStyle}>
            <div style={labelStyle}>
                {label}
            </div>
            <ThemeProvider theme={themeOptions}>
                <Slider
                    disabled={false}
                    max={100}
                    min={0}
                    value={value}
                    onChange={(event, newValue) => onChange(newValue)}
                    valueLabelDisplay="on"
                    style={sliderContainerStyles}
                    sx={sliderStyles}
                    valueLabelFormat={formatValueLabel}
                />
            </ThemeProvider>

        </div >

    )
}

export default LabeledSlider
