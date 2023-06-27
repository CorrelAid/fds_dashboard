<script>
    import { stats } from "../stores/stats.js";
    import Card from "./Card.svelte";
    import { formatAsPercent } from "./helpers/formatting.js";
</script>

<Card title={`Was ist der Stand von nicht abgeschlossenen Anfragen?`}>
    <ul>
        <li class="mb-2">
            <span class="h5">{$stats.foi_requests_not_resolved}</span> Anfragen laufen
            aktuell
        </li>
        <li class="mb-2">
            <span class="h5"
                >{formatAsPercent($stats.asleep_percentage_not_resolved)}</span
            >
            der laufenden und
            <span class="h5"
                >{formatAsPercent($stats.asleep_percentage_total)}</span
            > aller Anfragen sind eingeschlafen
        </li>
        <li class="mb-2">
            <span class="h5">{formatAsPercent($stats.overdue_percentage_not_resolved)}</span> der
            laufenden Anfragen sind verspätet
        </li>
    </ul>
</Card>
