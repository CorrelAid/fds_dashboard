import { writable,derived } from 'svelte/store';

export const selected_submit = writable(null);

const endpoint = "http://localhost:3000";

// processing the API data to be in a form thats convenient for using with d3
function proc_obj(obj) {
    let arr = []
    for (const [key, value] of Object.entries(obj)) {
        arr.push({ "value": value, "name": key })
    }

    // sorting values
    // arr.sort(function(x, y){
    //     return d3.descending(x.value, y.value);
    //  })
    //  console.log(arr)

    return arr
}

function proc_obj_time(obj){
    let arr = []
    let number = 0
    for (const [key, value] of Object.entries(obj)) {
        number = number + value
        arr.push({ "value": number, "name": key })
    }

    // requests by month will start in 2013
    // const dateParser = d3.timeParse("%Y-%m");
    // const cutoff = dateParser("2013-01");
    // arr = arr.filter(function(d) {
    //     const date = dateParser(d.name)
    //     return date > cutoff;
    //   })
    return arr
}

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

function translate_resolution(obj){
    const nw = {
        "null" : obj.None,
        "Rückzugsgrund Kosten": obj.user_withdrew_costs,
        "Zurückgezogen": obj.user_withdrew,
        "Erfolgreich": obj.successful,
        "Not held": obj.not_held,
        "Abgelehnt": obj.refused,
        "Teilweise erfolgreich": obj.partially_successful
    } 
    return nw
    }


function proc(data) {
    
    // extracting number of resolved foi requests
    data.foi_requests_resolved = data.stats_dist_status.resolved
    // extracting number of foi requests not resolved yet
    data.foi_requests_not_resolved = data.stats_foi_requests - data.foi_requests_resolved
    
    // calculating total success (rate)
    data.success = data.stats_dist_resolution.successful
    data.success_rate = Math.round((data.stats_dist_resolution.successful / data.stats_foi_requests) * 100)

    // processing status dist 
    // removing resolved foi requests from array
    
    // processing resolution dist
    // removing null (because these foi requests werent resolvey yet)
    data.dist_resolution = proc_obj(translate_resolution(data.stats_dist_resolution)).filter(data => data.name != 'null')

    // processing requests by month
    
    data.requests_by_month = proc_obj_time(data.stats_requests_by_month)
    return data
}

// The readable() function takes in the initial state of the store and a function that will be called once there is a first subscription (will not be called repeatedly)
export const stats = derived(selected_submit, ($selected_submit, set) => {
    fetch(endpoint).then(function (response) {
        if (!response.ok) {
            throw new Error('unable to load data');
        }
        return (response.json())}
    ).then(function (data) {
            console.log($selected_submit)
            const stats = proc(data)
            set(stats)
        })
}, null)
