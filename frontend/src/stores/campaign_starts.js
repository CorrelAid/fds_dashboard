import { _ } from "lodash";
import { readable} from 'svelte/store';

const endpoint = "http://localhost:3000/campaign_starts";


// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const campaign_starts = readable({}, function start(set) {
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())
    }
    ).then(function (data) {
        const starts = data
        set(starts)
    })

    return function stop() {

    };
})