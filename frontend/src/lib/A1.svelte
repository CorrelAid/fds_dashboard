<script>
    import Line from "./charts/Line.svelte";
    import Card from "./Card.svelte";
    import { total_stats } from "../stores/total_stats.js";
</script>

<Card
    title={"Wie viele Anfragen wurden gestellt?"}
>
    <Line data={$total_stats.total_requests_by_month} height={300} />
    <br />
    <p>
        <a href="https://fragdenstaat.de/anfragen/" class="h5"
            >Anfragen entdecken</a
        >
    </p>
</Card>
