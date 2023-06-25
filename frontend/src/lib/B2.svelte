<script>
    import { stats } from "../stores/stats.js";
    import Card from "./Card.svelte";
    import Balken from "./charts/Balken.svelte";
    import Donut from "./charts/Donut.svelte";
</script>

<Card title={`Was ist der Stand von nicht abgeschlossenen Anfragen?`}>
    <Donut data={$stats.dist_status} height={300} />
    <!-- <ul>
        <li class=""><span class="h5">{$stats.status_asleep}</span> Anfragen sind eingeschlafen.</li>
    </ul>    -->
</Card>
