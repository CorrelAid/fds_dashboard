<script>
    import { ranking } from "../stores/ranking.js";
    import Table from "./charts/Table.svelte";
    import Card from "./Card.svelte";
</script>

<Card title={"Jurisdiktionen"}>
    <Table data={$ranking} />
</Card>