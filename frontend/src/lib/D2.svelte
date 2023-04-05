<script>
    import { ranking_jurisdictions } from "../stores/ranking_jurisdictions.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
</script>

{#if $ranking_jurisdictions}
<Card title={"Jurisdiktionen"}>
    <Table data={$ranking_jurisdictions.ranking} />
</Card>
{/if}