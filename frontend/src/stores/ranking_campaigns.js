import { readable } from 'svelte/store';
import {api_url} from "../lib/data/data.js"


const endpoint = `${api_url}/ranking?typ=campaigns`


export const ranking_campaigns = readable(null, function start(set) {
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