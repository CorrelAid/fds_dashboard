<script>
  import { stats } from "./stores/stats.js";
  import { ranking_public_bodies } from "./stores/ranking_public_bodies.js";
  import { ranking_jurisdictions } from "./stores/ranking_jurisdictions.js";
  import { campaign_starts } from "./stores/campaign_starts.js";
  import Filter from "./lib/Filter.svelte";

  import LineRequests from "./lib/LineRequests.svelte";
  import DonutResolution from "./lib/DonutResolution.svelte";
  import Status from "./lib/Status.svelte";
  import ReactionTime from "./lib/ReactionTime.svelte";
  import Costs from "./lib/Costs.svelte";
  import RefusalReasons from "./lib/RefusalReasons.svelte";
  import RankingPublicBodies from "./lib/RankingPublicBodies.svelte";
  import RankingJurisdictions from "./lib/RankingJurisdictions.svelte";
  import RankingCampaigns from "./lib/RankingCampaigns.svelte";

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
        <LineRequests />
      </div>
    </div>
    <!-- B -->
    <div class="row">
      <div class="col-lg-7 p-3">
        <DonutResolution />
      </div>
      <div class="col-lg-5 p-3">
        <ReactionTime />
      </div>
    </div>
    <!-- C -->
    <div class="row">
      <div class="col-lg-6 p-3">
        <Status />
      </div>
      <div class="col-lg-6 p-3">
        <Costs />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <RefusalReasons />
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
        <RankingPublicBodies />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <RankingJurisdictions />
      </div>
    </div>
    <div class="row">
      <div class="col p-3">
        <RankingCampaigns />
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
