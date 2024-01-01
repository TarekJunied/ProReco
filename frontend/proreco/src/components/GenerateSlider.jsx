
import Slider from '@mui/material/Slider';
import { createTheme, ThemeProvider } from '@mui/material/styles';

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
    width: "36vw",
    margin: '0 auto', // Center the slider container
    position: "absolute",
    right: "10%"
};

const sliderStyles = {
    height: "3.7vh",
    borderRadius: "1.5vh",
};
/*
#FF7700 12.19%,
#FF6300 29.82%,
#FF4F00 51.94%,
#BF3604 90.29%);
*/
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

// eslint-disable-next-line react/prop-types
const GenerateSlider = ({ value, label, min, max, onChange, step }) => {



    // Custom format function to style the value label
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
                    max={max}
                    min={min}
                    value={value}
                    onChange={(event, newValue) => onChange(newValue)}
                    valueLabelDisplay="on"
                    step={step}
                    style={sliderContainerStyles}
                    sx={sliderStyles}
                    valueLabelFormat={formatValueLabel}
                />
            </ThemeProvider>

        </div>
    );
}

export default GenerateSlider;
