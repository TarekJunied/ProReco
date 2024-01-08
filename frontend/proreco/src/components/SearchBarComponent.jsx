
import React from 'react';
import { ReactSearchAutocomplete } from 'react-search-autocomplete';


const searchBarStyle = {
    width: "100%"
}

function SearchBarComponent(props) {

    const { items, onItemSelect } = props; // Accept an onItemSelect prop


    const handleOnSearch = (string, results) => {
        console.log(string, results);
    };

    const handleOnHover = (result) => {
        console.log(result);
    };

    const handleOnSelect = (item) => {
        console.log(item);
        if (onItemSelect) {
            onItemSelect(item.id); // Call the passed in onItemSelect function with the item id
        }
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
                    fontSize: "1.5vw",
                    zIndex: "1000"
                }}
            />

        </div>
    );
}

export default SearchBarComponent;
