import React from 'react'
import ChooseLayout from "../layout/ChooseLayout";
import SearchBarComponent from '../components/SearchBarComponent';
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'; // You can use Axios for making HTTP requests
import Swal from 'sweetalert2';
import InfoBox from '../components/InfoBox';
import FeatureInfoView from '../components/FeatureInfoView';


const FeaturerPage = () => {

    const [items, setItems] = useState([]);
    const [selectedItemIds, setSelectedItemIds] = useState(new Set());  // Track the IDs of selected items
    const [focusedItemId, setFocusedItemId] = useState(null);
    const itemRefs = useRef(new Map()); // To hold references to each item's div


    useEffect(() => {

        axios.post(`${import.meta.env.VITE_API_URL}/api/getFeatureList`)
            .then((response) => {

                const featureNames = response.data;

                // Creating an array of objects with id and name from each feature
                const formattedItems = featureNames.map((name, index) => {
                    return { id: index, name: name };
                });

                // Update the items state with the formatted items
                setItems(formattedItems);

                console.log("Formatted features:", formattedItems);


                const imageUrl = "https://proreco.co/cuteIcon.png"
                Swal.fire({
                    title: 'Success ! Feature Infos Arrived',
                    confirmButtonColor: '#BF3604',
                    imageUrl: imageUrl,
                    imageWidth: 250,
                    imageHeight: 250,
                    imageAlt: 'Custom image',
                    animation: true

                })
                console.log(response)
                console.log(response.data)

            })
            .catch((error) => {
                console.error("Error sending data to the backend:", error);
            });
    }, []); // The empty dependency array [] means this effect will run once after the initial render


    useEffect(() => {
        if (focusedItemId !== null && itemRefs.current.has(focusedItemId)) {
            itemRefs.current.get(focusedItemId).scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }
    }, [focusedItemId]);


    const handleButtonClick = (id) => {

        setFocusedItemId(id); // Set the focused item id

        if (itemRefs.current.has(id)) {
            itemRefs.current.get(id).scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }





        setSelectedItemIds(prevSelectedIds => {
            const newSelectedIds = new Set(prevSelectedIds); // Clone the previous state
            if (newSelectedIds.has(id)) {
                newSelectedIds.delete(id); // Remove the id if it's already selected
            } else {
                newSelectedIds.add(id); // Add the id if it's not selected
            }
            return newSelectedIds;
        });
    };

    return (
        <ChooseLayout>
            <InfoBox>

                <SearchBarComponent items={items}
                    onItemSelect={handleButtonClick} />
                <div>
                    {items.map((item) => (
                        <div key={item.id}
                            ref={(el) => itemRefs.current.set(item.id, el)} // Assign the div to the ref map
                        >
                            <button
                                onClick={() => handleButtonClick(item.id)}
                                style={{ display: 'block', margin: '10px 0' }}
                            >
                                {item.name}
                            </button>
                            {/* Check if item.id is in the selectedItemIds set to render FeatureInfoView */}
                            {selectedItemIds.has(item.id) &&


                                <FeatureInfoView item={item} />
                            }
                        </div>
                    ))}
                </div>
            </InfoBox>

        </ChooseLayout>
    )
}

export default FeaturerPage
