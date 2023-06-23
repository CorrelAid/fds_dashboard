<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { formatAsPercent, formatCosts } from "./helpers/formatting";
</script>

<Card title={"Wie teuer sind Anfragen?"}>
    <ul>
        <li>Bei <span class="h4">{formatAsPercent($stats.percentage_costs)}</span>
        der Anfragen stellt der Staat eine Rechnung. </li>
        <li>Daraufhin zogen <span class="h4">{formatAsPercent(
            $stats.percentage_withdrawn
        )}</span> der Nutzer*innen ihre Anfrage zurück.</li>
        <li> Wenn der Staat eine Rechnung stellt,
        verlangt er durchschnittlich <span class="h4">{formatCosts($stats.avg_costs)}</span>.</li> 
        <li>Die
        teuerste Rechnungsbetrag war <span class="h4">{formatCosts($stats.max_costs)}</span>.</li>
    </ul>
</Card>
