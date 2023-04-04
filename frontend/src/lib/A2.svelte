<script>
  import Balken from "./charts/Balken.svelte";
  import { stats } from "../stores/stats.js";
  import Card from "./Card.svelte";
  let data;
  data = $stats;
</script>

<Card title={"Wie enden Anfragen?"}>
<!-- <div>
  <p>Von <span class="h4">{data.stats_foi_requests_resolved}</span> abgeschlossenen
  Anfragen waren <span class="h4">{data.stats_success}</span>, also
  <span class="h4">{data.stats_success_rate}%</span> erfolgreich.</p>
<p>Die restlichen Anfragen endeten folgendermaßen:</p>
</div> -->
<Balken data = {$stats.dist_resolution}  height={400}/>
</Card>

