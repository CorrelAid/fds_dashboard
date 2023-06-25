<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { formatAsPercent, formatCosts } from "./helpers/formatting";
</script>

<Card title={"Wie teuer sind Anfragen?"}>
    <ul>
        <li class="mb-3">
            <span class="h5"
                >{formatAsPercent($stats.percentage_costs)}</span
            >
            der Anfragen kosten etwas.
        </li>
        <li class="mb-3">
            <span class="h5"
                >{formatAsPercent($stats.percentage_withdrawn)}</span
            > der Nutzer*innen zogen daraufhin ihre Anfrage zurück.
        </li>
        <li class="mb-3">
            <span
                class="h5">{formatCosts($stats.avg_costs)}</span
            > kosten Anfragen durchschnittlich, wenn der Staat Geld verlangt.
        </li>
        <li class="mb-3">
            <span class="h5"
                >{formatCosts($stats.max_costs)}</span
            > betrug die <a href="#">teuerste Rechnung</a>.
        </li>
    </ul>


</Card>
