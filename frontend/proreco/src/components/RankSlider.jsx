
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

// eslint-disable-next-line react/prop-types
const RankSlider = ({ value, onChange }) => {
    const sliderWidth = '70%';

    const sliderContainerStyles = {
        width: sliderWidth,
        margin: '0 auto', // Center the slider container
    };

    const sliderStyles = {
        height: 30,
        borderRadius: 2,
    };

    // Custom format function to style the value label
    const formatValueLabel = (value) => (
        <span style={{ fontFamily: 'outfit', fontSize: '20px' }}>{value}</span>
    );

    return (
        <div className="flex items-center justify-center mb-5"> {/* Reduce the margin-bottom to align the items better */}
            <ThemeProvider theme={themeOptions}>
                <Slider
                    disabled={false}
                    max={100}
                    min={0}
                    size="large"
                    value={value}
                    onChange={(event, newValue) => onChange(newValue)}
                    valueLabelDisplay="on"
                    style={sliderContainerStyles}
                    sx={sliderStyles}
                    valueLabelFormat={formatValueLabel}
                />
            </ThemeProvider>
        </div>
    );
}

export default RankSlider;
