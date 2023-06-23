<script>
    import { stats } from "../stores/stats.js";
    import Balken from "./charts/Balken.svelte";
    import Card from "./Card.svelte";
    import { roundNumber } from "./helpers/formatting";
</script>
<Card title={"Wie schnell ist der Staat durchschnittlich?"}>
    <ul>
        <li> Bis zu eine ersten Antwort dauert es <span class="h4">{roundNumber($stats.initial_reaction_time,0)} Tage</span></li>
        <li> Anfragen sind nach <span class="h4">{roundNumber($stats.resolved_time,0)} Tagen</span> abgeschlossen.</li>
    </ul>
</Card>
