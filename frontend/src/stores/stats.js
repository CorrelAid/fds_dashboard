import { writable,derived } from 'svelte/store';

export const url_params = writable(null);


let endpoint = "http://localhost:3000";

// function translate_status(obj){
// const nw = {
//     "Eingeschlafen" : obj.asleep,
//     "Verspätet": obj.overdue,
//     "Abgeschlossen": obj.resolved,
//     "Public Body needed": obj.publicbody_needed,
//     "Keine Klassifizierung": obj.awaiting_classification,
//     "Keine Nutzerbestätigung": obj.awaiting_user_confirmation,
//     "Wartet auf Antwort": obj.awaiting_response
// } 
// return nw
// }

// function translate_resolution(obj){
//     const nw = {
//         "null" : obj.None,
//         "Rückzugsgrund Kosten": obj.user_withdrew_costs,
//         "Zurückgezogen": obj.user_withdrew,
//         "Erfolgreich": obj.successful,
//         "Not held": obj.not_held,
//         "Abgelehnt": obj.refused,
//         "Teilweise erfolgreich": obj.partially_successful
//     } 
//     return nw
//     }



// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const stats = derived(url_params, ($url_params, set) => {
    if ($url_params != null){
        console.log($url_params)
        // endpoint = endpoint + url_params
    }
    else{
        endpoint = endpoint
    }
    
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())}
    ).then(function (data) {
            
            const stats = data
            set(stats)
        })
}, null)
