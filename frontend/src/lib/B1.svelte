<script>
    import { stats } from "../stores/stats.js";
    import Balken from "./charts/Balken.svelte";
    import Card from "./Card.svelte";
</script>

<Card title={"Was ist der Status der momentan laufenden Anfragen?"}>
<p>Von den <span class="h4">{$stats.stats_foi_requests_not_resolved}</span> Anfragen, die aktuell bearbeitet werden,</p>

<ul>
    <li> warten <span class="h4">{$stats.stats_dist_status.overdue}</span> noch auf eine Antwort.</li>
    <li> sind <span class="h4">{$stats.stats_dist_status.awaiting_response}</span> über der Frist.</li>
    <li> sind <span class="h4">{$stats.stats_dist_status.asleep}</span> eingeschlafen.</li>
</ul>
</Card>

