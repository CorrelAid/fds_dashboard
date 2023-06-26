<script>
    import Line from "./charts/Line.svelte";
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { campaign_starts } from "../stores/campaign_starts.js";
    import { url_params } from "../stores/stats.js";
    import { general_info } from "../stores/general_info.js";

    let requests_by_month;
    $: requests_by_month = $stats.requests_by_month;

    function url_string(str) {
        const temp = str
            .toLowerCase()
            .replace(/ä/g, "ae")
            .replace(/ö/g, "oe")
            .replace(/ü/g, "ue")
            .replace(/ß/g, "ss")
            .replace(/!/g, '')
            .replace(/[^a-z0-9]+/g, '-');
        return temp;
    }

    function extractValuesFromURL(url) {
        var urlParams = new URLSearchParams(url);
        var category = urlParams.get("category");
        var selection = urlParams.get("selection");

        return {
            category: category,
            selection: selection,
        };
    }
    let explore_url = "https://fragdenstaat.de/anfragen/";

    $: values = extractValuesFromURL($url_params);

    $: category = values.category;
    $: id = values.selection;

    $: if (category === "public_body_id") {
        explore_url = `https://fragdenstaat.de/behoerde/${id}`;
    } else if (category === "jurisdiction_id" && id) {
        const filteredObject = $general_info.jurisdictions.find(
            (obj) => obj.id === parseInt(id)
        ).name;
        const str = url_string(filteredObject)
        explore_url = `https://fragdenstaat.de/anfragen?jurisdiction=${str}`;
    } else if (category === "campaign_id" && id) {
        const filteredObject = $general_info.campaigns.find(
            (obj) => obj.id === parseInt(id)
        ).name;
        const str = url_string(filteredObject)
        explore_url = `https://fragdenstaat.de/anfragen?campaign=${str}`;
    } else if (category === null) {
        explore_url = "https://fragdenstaat.de/anfragen/"
    }

</script>

<Card title={"Wie viele Anfragen wurden gestellt?"}>
    <Line
        data={requests_by_month}
        x_labels={$campaign_starts.campaign_starts}
        height={300}
    />
    <br />
    <p>
        <a href={explore_url} target="_blank" class="btn btn-primary">Anfragen entdecken</a>
    </p>
</Card>
