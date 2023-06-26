<script>
    import { stats } from "../stores/stats.js";
    import Balken from "./charts/Balken.svelte";
    import Card from "./Card.svelte";
    import { roundNumber,formatAsPercent } from "./helpers/formatting.js";
</script>
<Card title={"Wie schnell ist der Staat?"}>
    <ul>
        <li class="mb-2"><span class="h5">{roundNumber($stats.resolved_time,2)}</span> Tage dauert es durchschnittlich, bis Anfragen abgeschlossen sind.</li>
        <li class="mb-2"><span class="h5">{roundNumber($stats.initial_reaction_time,2)}</span> Tage braucht der Staat durchschnittlich bis zu einer ersten Antwort.</li>
        <li class="mb-2"><span class="h5">{formatAsPercent($stats.overdue_rate,2)}</span> aller Anfragen waren verspätet.</li>
    </ul>
</Card>
