import React from 'react'
import InfoBox from './InfoBox'

const categoryStyle = {
    color: "#7C1C0B",
    textTransform: 'uppercase'


}

const FeatureInfoView = ({ item }) => {
    return (

        <InfoBox >

            <div style={{ padding: '20px', marginTop: '10px' }}>
                <h3>
                    <span style={categoryStyle}>Name:</span> {item.name}
                </h3>
                <h3>
                    <span style={categoryStyle}>Description:</span> {item.description}
                </h3>
                <h3>
                    <span style={categoryStyle}>From:</span> {item.from}
                </h3>
                <h3>
                    <span style={categoryStyle}>Used in:</span> {item.no_regressors} regressors
                </h3>
                <h3>
                    <span style={categoryStyle}>Most important for :</span> {item.most_important_regressor}
                </h3>
                <h3>
                    <span style={categoryStyle}>Ranking:</span> {item.feature_ranking}
                </h3>
                <h3>
                    <span style={categoryStyle}>Feature Score:</span> {item.feature_importance_points}
                </h3>

                {/* You might include more detailed information here */}
            </div>
        </InfoBox >

    )
}

export default FeatureInfoView
