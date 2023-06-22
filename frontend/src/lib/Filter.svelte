<script>
    import { clickOutside } from "./helpers/clickOutside";
    import Lense from "./svg/Lense.svelte";
    import Dropdown from "./svg/Dropdown.svelte";
    import { url_params } from "../stores/stats.js";
    import { term, category, filtered } from "../stores/general_info.js";
    let show = "";
    let selected = null;

    const toggle = () => {
        show == "" ? (show = "show") : (show = "");
    };

    function set_url_params(selected) {
        if (selected != null) {
            const tr = {
                jurisdictions: "jurisdiction_id",
                public_bodies: "public_body_id",
                campaigns: "campaign_id",
            };
            $url_params = `?l=${tr[$category]}&s=${selected}`;
        } else {
            $url_params = "";
        }
    }
</script>

<div class="container">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-center align-items-center pt-4">
                <ul class="nav nav-pills">
                    <!-- <li class="nav-item">
                      <button class="nav-link {$category=="all"?"active":""}" on:click={()=> {$category="all"}}>Alle</button>
                    </li> -->
                    <li class="nav-item">
                        <button
                            class="nav-link {$category == 'public_bodies'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                ($category = "public_bodies"),
                                    (selected = ""),
                                    ($term = "");
                            }}>Behörden</button
                        >
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link {$category == 'jurisdictions'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                ($category = "jurisdictions"),
                                    (selected = ""),
                                    ($term = "");
                            }}>Jurisdiktionen</button
                        >
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link {$category == 'campaigns'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                ($category = "campaigns"),
                                    (selected = ""),
                                    ($term = "");
                            }}>Kampagnen</button
                        >
                    </li>
                </ul>
            </div>
        </div>

        <div
            class="col-12 d-flex justify-content-center align-items-center py-4"
        >
            <div
                class="dropdown show"
                use:clickOutside
                on:click_outside={show === "show" ? toggle() : null}
            >
                <div
                    class="d-flex justify-content-center align-items-center"
                    style="height: 40px;"
                >
                    <span
                        class="bg-white h-100 d-flex justify-content-center align-items-center"
                    >
                        <Lense height={22} width={30} />
                    </span>
                    <input
                        type="text"
                        class="search"
                        aria-disabled={$category === "all" ? "true" : "false"}
                        placeholder={$category === "all"
                            ? "Kategorie auswählen..."
                            : "Suchen..."}
                        on:focus={show === "" && $category !== "all"
                            ? toggle()
                            : null}
                        bind:value={$term}
                    />
                    <span
                        class="bg-white h-100 d-flex justify-content-center align-items-center"
                        on:click={() => {
                            $category !== "all" ? toggle() : null;
                        }}
                    >
                        <Dropdown height={22} width={30} />
                    </span>
                    <button
                        type="button"
                        class="btn fw-normal btn-primary ms-3 h-100 d-flex justify-content-center align-items-center"
                        on:click={() => {
                            set_url_params(selected);
                        }}>Anzeigen</button
                    >
                </div>

                <div
                    class="dropdown-menu {show}"
                    aria-labelledby="dropdownMenuLink"
                >
                    <span
                        class="dropdown-item"
                        on:click={() => {
                            (selected = null), (show = ""), ($term = "");
                        }}>Alle</span
                    >
                    {#each $filtered as item}
                        <span
                            class="dropdown-item"
                            on:click={() => {
                                (selected = item.id),
                                    (show = ""),
                                    ($term = item.name);
                            }}>{item.name}</span
                        >
                    {/each}
                </div>
            </div>
        </div>
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

    /* .search[aria-disabled="true"] {
        background-color: white;
        cursor:not-allowed;
        pointer-events: unset;
    } */
</style>
