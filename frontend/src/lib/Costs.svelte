<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import Box from "./charts/Box.svelte";
    import { formatAsPercent, formatCosts } from "./helpers/formatting";

    $: max_costs_url = `https://fragdenstaat.de/api/v1/request/${$stats.costs[0].Max.id}/`
</script>

<Card title={"Wie teuer sind Anfragen?"}>
    {#if $stats.percentage_costs != 0}
    <Box data={$stats.costs[0]} height={180} unit={"Euro"} name={"Kosten"} decimal_Places={2}/>
    {/if}
    <ul>
        <li class="mb-3 {$stats.percentage_costs != 0 ? "mt-5" : ""}">
            <span class="h5"
                >{formatAsPercent($stats.percentage_costs)}</span
            >
            der Anfragen kosten etwas.
        </li>
        {#if $stats.percentage_costs != 0}
        <li class="mb-3">
            <span class="h5"
                >{formatAsPercent($stats.percentage_withdrawn)}</span
            > der Nutzer*innen zogen daraufhin ihre Anfrage zurück.
        </li>
        {/if}
    </ul>


</Card>
