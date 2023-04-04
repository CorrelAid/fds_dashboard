import { readable } from 'svelte/store';

const endpoint = "http://localhost:3000/general_info";


// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const general_info = readable([], function start(set) {
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())
    }
    ).then(function (data) {
        const general_info = data
        set(general_info)
    })

    return function stop() {

    };
})
