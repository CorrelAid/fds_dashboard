<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { formatAsPercent } from "./helpers/formatting";
</script>

<Card title={"Wie teuer sind Anfragen?"}>
    <p>Die Kosten, die <span class="h4">{formatAsPercent($stats.percentage_costs)}</span> der Anfragen generieren, verteilen sich folgendermaßen:</p>
</Card>

