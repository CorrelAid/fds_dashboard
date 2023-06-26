<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
</script>

<Card title={"Warum lehnt der Staat Anfragen ab?"}>
    <ul>
        <li></li>
        {#each $stats.refusal_reasons as item}
            <li>{item.reason}</li>
        {/each}
    </ul>
</Card>
