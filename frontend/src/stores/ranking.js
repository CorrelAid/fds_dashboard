import { readable } from 'svelte/store';

const endpoint = "http://localhost:3000/ranking_public_body";

function proc_rankings(data) {
    data.public_bodies = data.public_bodies
    data.jurisdictions = data.jurisdictions
    return data
}

export const ranking = readable(null, function start(set) {
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())
    }
    ).then(function (data) {
        set(data)
    })

    return function stop() {
        console.log('Store Stopped');
    };
})