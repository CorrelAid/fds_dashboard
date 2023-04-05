import { readable } from 'svelte/store';

const endpoint = "http://localhost:3000/ranking?typ=public_bodies";


export const ranking_public_bodies = readable(null, function start(set) {
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