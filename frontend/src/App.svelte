<script>
  import { stats } from "./stores/stats.js";
  import { ranking_public_bodies } from "./stores/ranking_public_bodies.js";
  import { ranking_jurisdictions } from "./stores/ranking_jurisdictions.js";
  import { campaign_starts } from "./stores/campaign_starts.js";
  import Filter from "./lib/Filter.svelte";

  import A from "./lib/A.svelte";
  import B1 from "./lib/B1.svelte";
  import B2 from "./lib/B2.svelte";
  import C1 from "./lib/C1.svelte";
  import C2 from "./lib/C2.svelte";
  import D from "./lib/D.svelte";
  import E1 from "./lib/E1.svelte";
  import E2 from "./lib/E2.svelte";
  import E3 from "./lib/E3.svelte";
</script>

<!-- Before rendering components, subscribe to store (make api call) and check if data is loaded -->
{#if !$stats | !$campaign_starts | !$ranking_jurisdictions | !$ranking_public_bodies}
  <h2>Loading...</h2>
{:else}
  <div class="text-center p-3">
    <h2 class="my-4">FragDenStaat Statistikzentrum</h2>
  </div>
  <div class="container border-blue shadow-blue">
    <div class="row">
      <div class="col">
        <Filter />
      </div>
    </div>
    <!-- A -->
    <div class="row">
      <div class="col p-3">
        <A />
      </div>
    </div>
    <!-- B -->
    <div class="row">
      <div class="col-lg-7 p-3">
        <B1 />
      </div>
      <div class="col-lg-5 p-3">
        <C1 />
      </div>
    </div>
    <!-- C -->
    <div class="row">
      <div class="col-lg-7 p-3">
        <B2 />
      </div>
      <div class="col-lg-5 p-3">
        <C2 />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <D />
      </div>
    </div>
  </div>

  <!-- D -->
  <div class="container mt-6 border-blue shadow-blue mb-5">
    <div class="row ranking px-3 py-4">
      <h3 class="">Rankings</h3>
    </div>
    <div class="row">
      <div class="col p-3">
        <E1 />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <E2 />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <E3 />
      </div>
    </div>
  </div>
{/if}

<style>
  .col {
    padding: 0;
  }
  .ranking {
    background-color: #b6ddf5;
  }
</style>
