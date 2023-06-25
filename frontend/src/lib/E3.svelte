<script>
    import { ranking_campaigns, values_campaigns } from "../stores/ranking_campaigns.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
    let values;


    $: $values_campaigns = values;
</script>

{#if $ranking_campaigns}
<Card title={"Kampagnen"}>
    <Table data={$ranking_campaigns.ranking} bind:values type={"campaigns"}/>
</Card>
{/if}