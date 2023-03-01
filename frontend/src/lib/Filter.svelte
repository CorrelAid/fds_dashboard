<script>
    export let jurisdictions = [];
    let selected = 0;
    const filter_height = 50;
</script>

<div class="container">
    <div class="row">
        <div
            class="col-12  d-flex justify-content-center align-items-center py-3">
            <div class="">
                <span class="pr-2 h5 m-0">Statistiken anzeigen für:</span>
                <select
                    bind:value={selected}
                    class="form-select h5 fw-light p-0"
                    aria-label="Default select example"
                >
                    <option value={0}>Kein Filter</option>
                    <option value={1}>Jurisdiktion</option>
                    <option value={2}>Behörde</option>
                </select>
            </div>
        </div>
        {#if selected != 0}
            <div
                class="col-12  d-flex justify-content-center align-items-center py-3"
            >
                {#if selected == 1}
                    <select
                        class="form-select h5"
                        aria-label="Default select example"
                    >
                        <option value="0" selected>Alle Jurisdiktionen</option>
                        {#each Object.values(jurisdictions) as jurisdiction, index}
                            <option value={index + 1}>{jurisdiction}</option>
                        {/each}
                    </select>
                {/if}
                {#if selected == 2}
                    <input type="text" id="" placeholder="Alle Behörden" />
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .container {
        background-color: #b6ddf5;
    }
</style>
