<script>
  import Donut from "./charts/Donut.svelte";
  import { stats } from "../stores/stats.js";
  import Card from "./Card.svelte";
  let data;
  data = $stats;
</script>

<Card title={"Wie enden Anfragen?"}>
<Donut data = {$stats.dist_resolution}  height={400} centerNumber={$stats.foi_requests_resolved}/>
</Card>

