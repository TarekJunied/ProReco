import React from 'react'
import InfoBox from './InfoBox'

const FeatureInfoView = ({ item }) => {
    return (

        <InfoBox >

            <div style={{ padding: '20px', marginTop: '10px' }}>
                <h3>Details for: {item.name}</h3>
                {/* You might include more detailed information here */}
            </div>
        </InfoBox >

    )
}

export default FeatureInfoView
