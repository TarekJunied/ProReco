import React from 'react'
import ChooseLayout from "../layout/ChooseLayout";
import SearchBarComponent from '../components/SearchBarComponent';
import { useState, useEffect } from 'react'
import axios from 'axios'; // You can use Axios for making HTTP requests
import Swal from 'sweetalert2';
import InfoBox from '../components/InfoBox';


const FeaturerPage = () => {

    const [items, setItems] = useState([]);

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




    return (
        <ChooseLayout>
            <InfoBox>
                <SearchBarComponent items={items} />

            </InfoBox>
        </ChooseLayout>
    )
}

export default FeaturerPage
