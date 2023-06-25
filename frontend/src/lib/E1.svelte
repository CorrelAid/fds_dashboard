<script>
    import { ranking_public_bodies, values_public_bodies } from "../stores/ranking_public_bodies.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
    let values;


    $: $values_public_bodies = values;
</script>

{#if $ranking_public_bodies}
<Card title={"Behörden"}>
    <Table data={$ranking_public_bodies.ranking} bind:values/>
</Card>
{/if}