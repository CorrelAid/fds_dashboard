import { readable, writable, derived } from 'svelte/store';
import { _ } from "lodash";
import {api_url} from "../lib/data/data.js"

export const url_params = writable(null);

const endpoint = `${api_url}/ranking?category=public_bodies`
let temp_endpoint = endpoint;

export const values_public_bodies = writable();

export const ranking_public_bodies = derived(values_public_bodies, ($values_public_bodies, set) => {
    if ($values_public_bodies != null){
        for (const key in $values_public_bodies) {
            if ($values_public_bodies[key].selected === true) {
                let str = $values_public_bodies[key].ascending.toString()
                str = str.replace(str[0], str[0].toUpperCase())
                temp_endpoint = `${endpoint}&ascending=${str}&selection=${key}`
            }
          }
        
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
            const ranking = data
            set(ranking)
        })
}, null)


// "Anzahl", "Erfolgsquote", "Verspaetungsquote", "Abgeschlossenenquote
