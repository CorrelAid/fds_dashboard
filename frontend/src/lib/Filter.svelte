<script>
    import { clickOutside } from "./helpers/clickOutside";
    import Lense from "./svg/Lense.svelte";
    import Dropdown from "./svg/Dropdown.svelte";
    export let jurisdictions = [];
    let scoops;
    let selected = 0;
    const filter_height = 50;
    let show_type = "";

    const toggle_type = () => {
        show_type == "" ? (show_type = "show") : (show_type = "");
    };
</script>

<div class="container">
    <div class="row">
        <div class="col-12">
            <p class="h5 text-center pt-2 pb-3">Statistiken anzeigen für:</p>
            <div class="d-flex justify-content-center align-items-center">
                <label >
                    <input
                        type="radio"
                        bind:group={scoops}
                        name="scoops"
                        value={1}
                    />
                    Jurisdiktionen
                </label>

                <label class="px-2">
                    <input
                        type="radio"
                        bind:group={scoops}
                        name="scoops"
                        value={2}
                    />
                    Behörden
                </label>

                <label class="px-2">
                    <input
                        type="radio"
                        bind:group={scoops}
                        name="scoops"
                        value={3}
                    />
                    Kampagnen
                </label>
            </div>
        </div>

        <!-- {#if selected != 0} -->
        <div
            class="col-12  d-flex justify-content-center align-items-center py-4"
        >
            <div
                class="dropdown show"
                use:clickOutside
                on:click_outside={show_type === "show" ? toggle_type() : null}
            >
                <div
                    class="d-flex justify-content-center align-items-center "
                    style="height: 30px;"
                >
                    <span class="bg-white h-100">
                        <Lense height={22} width={30} />
                    </span>
                    <input type="text" class="search" placeholder="Search.." />
                    <span class="bg-white h-100" on:click={toggle_type}>
                        <Dropdown height={22} width={30} />
                    </span>
                </div>

                <div
                    class="dropdown-menu {show_type}"
                    aria-labelledby="dropdownMenuLink"
                >
                    <a class="dropdown-item" href="#">Action</a>
                    <a class="dropdown-item" href="#">Another action</a>
                    <a class="dropdown-item" href="#">Something else here</a>
                </div>
            </div>
            <!-- {#if selected == 1} -->
            <!-- <select
                        class="form-select h5"
                        aria-label="Default select example"
                    >
                        <option value="0" selected>Alle Jurisdiktionen</option>
                        {#each Object.values(jurisdictions) as jurisdiction, index}
                            <option value={index + 1}>{jurisdiction}</option>
                        {/each}
                    </select> -->
            <!-- {/if}
                {#if selected == 2} -->
            <!-- <input type="text" id="" placeholder="Alle Behörden" /> -->
            <!-- {/if} -->
        </div>
        <!-- {/if} -->
    </div>
</div>

<style>
    .container {
        background-color: #b6ddf5;
    }
    .search {
        border: none;
        padding: 0;
        height: 100%;
    }
    .search:focus {
        outline: none;
    }
</style>
