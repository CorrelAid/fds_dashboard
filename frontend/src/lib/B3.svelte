<script>
     import { stats } from "../stores/stats.js";
    import Card from "./Card.svelte";
    import { formatAsPercent } from "./helpers/formatting";
</script>

<Card title={`Wie viele registrierte Nutzer gibt es?`}>
    <ul>
        <li class="mb-2">
            <span class="h5">{$stats.users}</span> Menschen nutzen FragDenStaat.
        </li>
    </ul>
</Card>
