<script>
    import { ranking_campaigns } from "../stores/ranking_campaigns.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
</script>

{#if $ranking_campaigns}
<Card title={"Kampagnen"}>
    <Table data={$ranking_campaigns.ranking} />
</Card>
{/if}