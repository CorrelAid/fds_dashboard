<script>
    import { stats } from "../stores/stats.js";
    import Balken from "./charts/Balken.svelte";
    import Card from "./Card.svelte";
    import { roundNumber } from "./helpers/formatting";
</script>
<Card title={"Wie schnell ist der Staat durchschnittlich?"}>
    <ul>
        <li class="mb-2"> Bis zu eine ersten Antwort dauert es <span class="h5">{roundNumber($stats.initial_reaction_time,0)}</span> Tage</li>
        <li class="mb-2"> Anfragen sind nach <span class="h5">{roundNumber($stats.resolved_time,0)}</span> Tagen abgeschlossen.</li>
    </ul>
</Card>
