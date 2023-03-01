<script>
  import Balken from "./charts/Balken.svelte";
  import { total_stats } from "../stores/total_stats.js";
  import Card from "./Card.svelte";
  let data;
  data = $total_stats;
</script>

<Card title={"Wie enden Anfragen?"}>
<!-- <div>
  <p>Von <span class="h4">{data.total_foi_requests_resolved}</span> abgeschlossenen
  Anfragen waren <span class="h4">{data.total_success}</span>, also
  <span class="h4">{data.total_success_rate}%</span> erfolgreich.</p>
<p>Die restlichen Anfragen endeten folgendermaßen:</p>
</div> -->
<Balken data = {$total_stats.total_dist_resolution}  height={400}/>
</Card>

