<script>
    import Line from "./charts/Line.svelte";
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { campaign_starts } from "../stores/campaign_starts.js";
  
    let requests_by_month;
    $: requests_by_month = $stats.requests_by_month;
    // $: console.log(requests_by_month)
</script>

<Card
    title={"Wie viele Anfragen wurden gestellt?"}
>
    <Line data={requests_by_month} x_labels={$campaign_starts.campaign_starts} height={300} />
    <br />
    <p>
        <a href="https://fragdenstaat.de/anfragen/" class="btn btn-primary"
            >Anfragen entdecken</a
        >
    </p>
</Card>
