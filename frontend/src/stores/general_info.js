import { _ } from "lodash";
import { readable, writable, derived } from 'svelte/store';

const endpoint = "http://localhost:3000/general_info";


// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const general_info = readable({}, function start(set) {
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

export const term = writable('');
export const category = writable('public_bodies');

export const filtered = derived(
    [term, general_info, category], ([$term, $general_info, $category], set) => {
        if (_.isEmpty($general_info) === false) {
            let lst = Object.values($general_info[$category])
            // let result = _.find(songs, {id});
            let result = lst.filter(x => x.includes($term))
            set(result.slice(0, 10))
        }

    }, [])

