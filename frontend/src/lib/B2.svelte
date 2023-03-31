<script>
    import { stats } from "../stores/stats.js";
    import Balken from "./charts/Balken.svelte";
    import Card from "./Card.svelte";

</script>
<Card title={"Wie schnell ist der Staat durchschnittlich?"}>
    <ul>
        <li> Bis zu eine ersten Antwort dauert es <span class="h4">3 Tage</span></li>
        <li> Generell benötigt der Staat <span class="h4">5 Tage</span> um zu antworten.</li>
        <li> Anfragen sind nach <span class="h4">30 Tagen</span> abgeschlossen.</li>
        <li><span class="h4">34%</span> aller Anfragen werden verspätet abgeschlossen.</li>
    </ul>
</Card>
