import { writable,derived } from 'svelte/store';
import {api_url} from "../lib/data/data.js"

const endpoint = `${api_url}`

export const url_params = writable(null);


let temp_endpoint = endpoint;

// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const stats = derived(url_params, ($url_params, set) => {
    if ($url_params != null){
        temp_endpoint = endpoint + $url_params
    }
    else{
        temp_endpoint = endpoint
    }
    fetch(temp_endpoint).then(function (response) {
        
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())}
    ).then(function (data) {
            
            const stats = data
         
           
            set(stats)
        })
}, null)
