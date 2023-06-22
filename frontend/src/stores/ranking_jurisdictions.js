import { readable, writable, derived } from 'svelte/store';
import { _ } from "lodash";
import {api_url} from "../lib/data/data.js"

export const url_params = writable(null);

const endpoint = `${api_url}/ranking?typ=jurisdictions`
let temp_endpoint = endpoint;

export const values_jurisdictions = writable();

export const ranking_jurisdictions = derived(values_jurisdictions, ($values_jurisdictions, set) => {
    if ($values_jurisdictions != null){
        console.log($values_jurisdictions)
        for (const key in $values_jurisdictions) {
            if ($values_jurisdictions[key].selected === true) {
                let str = $values_jurisdictions[key].ascending.toString()
                str = str.replace(str[0], str[0].toUpperCase())
                temp_endpoint = `${endpoint}&ascending=${str}&s=${key}`
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
