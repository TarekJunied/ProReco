
import React from 'react';
import { ReactSearchAutocomplete } from 'react-search-autocomplete';


const searchBarStyle = {
    width: "100%"
}

function SearchBarComponent(props) {
    const { items } = props;

    const handleOnSearch = (string, results) => {
        console.log(string, results);
    };

    const handleOnHover = (result) => {
        console.log(result);
    };

    const handleOnSelect = (item) => {
        console.log(item);
    };

    const handleOnFocus = () => {
        console.log('Focused');
    };

    const formatResult = (item) => {
        return (
            <>
                <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
                <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span>
            </>
        );
    };

    return (
        <div style={searchBarStyle}>
            <ReactSearchAutocomplete
                items={items}
                onSearch={handleOnSearch}
                onHover={handleOnHover}
                onSelect={handleOnSelect}
                onFocus={handleOnFocus}
                autoFocus
                formatResult={formatResult}
                styling={{
                    fontFamily: "outfit",
                    fontSize: "1.2vw"
                }}
            />
        </div>
    );
}

export default SearchBarComponent;
