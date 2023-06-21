import { readable } from 'svelte/store';

const endpoint = "http://127.0.0.1:8000/ranking?typ=jurisdictions";


export const ranking_jurisdictions = readable(null, function start(set) {
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())
    }
    ).then(function (data) {
        const ranking = data
        
        set(ranking)
    })

    return function stop() {
        console.log('Store Stopped');
    };
})