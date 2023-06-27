<script>
    import { stats } from "../stores/stats.js";
    import Box from "./charts/Box.svelte";
    import Card from "./Card.svelte";
    import { roundNumber,formatAsPercent } from "./helpers/formatting.js";
</script>
<Card title={"Wie schnell ist der Staat?"}>
    <Box data={$stats.resolved_time[0]} height={180} unit={"Tage"} name={"Abschlussdauer"} decimal_Places={0} type={"time"}/>
    <ul>
        <li class="mb-2 mt-5"><span class="h5">{formatAsPercent($stats.overdue_rate,2)}</span> aller Anfragen waren verspätet.</li>
        <li class="mb-2"><span class="h5">{roundNumber($stats.initial_reaction_time[0].Average,2)}</span> Tage braucht der Staat durchschnittlich bis zu einer ersten Antwort.</li>
    </ul>
</Card>
