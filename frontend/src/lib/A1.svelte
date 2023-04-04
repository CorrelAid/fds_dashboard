<script>
    import Line from "./charts/Line.svelte";
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
  
</script>

<Card
    title={"Wie viele Anfragen wurden gestellt?"}
>
    <Line data={$stats.requests_by_month} height={300} />
    <br />
    <p>
        <a href="https://fragdenstaat.de/anfragen/" class="h5"
            >Anfragen entdecken</a
        >
    </p>
</Card>
