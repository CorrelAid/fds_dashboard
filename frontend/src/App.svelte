<script>
  import { stats } from "./stores/stats.js";;
  import Filter from "./lib/Filter.svelte";

  import A from "./lib/A.svelte";
  import A2 from "./lib/A2.svelte";
  import B1 from "./lib/B1.svelte";
  import B2 from "./lib/B2.svelte";
  import C1 from "./lib/C1.svelte";
  import C2 from "./lib/C2.svelte";
  import D1 from "./lib/D1.svelte";
  import D2 from "./lib/D2.svelte";
</script>

<!-- Before rendering components, subscribe to store (make api call) and check if data is loaded -->
{#if !$stats}
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
      <div class="col p-3">
        <A2 />
      </div>
      <div class="col p-3">
        <B1 />
      </div>
    </div>
    <!-- C -->
    <div class="row">
      <div class="col p-3">
        <B2 />
      </div>
      <div class="col p-3">
        <C1 />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <C2 />
      </div>
    </div>
  </div>
  
{/if}
<!-- D -->
  <div class="container mt-6 border-blue shadow-blue mb-5">
    <div class="row ranking px-3 py-4">
      <h3 class="">Rankings</h3>
    </div>
    <div class="row ">
      <div class="col p-3">
        <D1 />
      </div>
    </div> 
<div class="row ">
      <div class="col p-3">
        <D2 />
      </div>
    </div>
</div>

<style>
  .col {
    padding: 0;
  }
  .ranking {
    background-color: #b6ddf5;
  }
</style>
