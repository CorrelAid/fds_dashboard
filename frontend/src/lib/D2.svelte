<script>
    import { ranking_jurisdictions, values_jurisdictions } from "../stores/ranking_jurisdictions.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
    let values;
    $: console.log($ranking_jurisdictions)

    $: $values_jurisdictions = values;
</script>

{#if $ranking_jurisdictions}
<Card title={"Jurisdiktionen"}>
    <Table data={$ranking_jurisdictions.ranking} bind:values/>
</Card>
{/if}