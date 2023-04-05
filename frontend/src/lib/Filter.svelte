<script>
    import { clickOutside } from "./helpers/clickOutside";
    import Lense from "./svg/Lense.svelte";
    import Dropdown from "./svg/Dropdown.svelte";
    import { selected_submit } from "../stores/stats.js";
    import { general_info } from "../stores/general_info.js";
    let type = "public_body";
    let show = "";
    let selected = null;

    const toggle = () => {
        show == "" ? (show = "show") : (show = "");
    };
</script>

<div class="container">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-center align-items-center pt-4">
                <ul class="nav nav-pills">
                    <!-- <li class="nav-item">
                      <button class="nav-link {type=="all"?"active":""}" on:click={()=> {type="all"}}>Alle</button>
                    </li> -->
                    <li class="nav-item">
                        <button
                            class="nav-link  {type == 'public_body'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                (type = "public_body"), (selected = "");
                            }}>Behörden</button
                        >
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link {type == 'jurisdiction'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                (type = "jurisdiction"), (selected = "");
                            }}>Jurisdiktionen</button
                        >
                    </li>
                    <li class="nav-item">
                        <button
                            class="nav-link {type == 'campaign'
                                ? 'active'
                                : ''}"
                            on:click={() => {
                                (type = "campaign"), (selected = "");
                            }}>Kampagnen</button
                        >
                    </li>
                </ul>
            </div>
        </div>

        <div
            class="col-12  d-flex justify-content-center align-items-center py-4"
        >
            <div
                class="dropdown show"
                use:clickOutside
                on:click_outside={show === "show" ? toggle() : null}
            >
                <div
                    class="d-flex justify-content-center align-items-center "
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
                        aria-disabled={type === "all" ? "true" : "false"}
                        placeholder={type === "all"
                            ? "Kategorie auswählen..."
                            : "Suchen..."}
                        on:focus={show === "" && type !== "all"
                            ? toggle()
                            : null}
                        bind:value={selected}
                    />
                    <span
                        class="bg-white h-100 d-flex justify-content-center align-items-center"
                        on:click={() => {
                            type !== "all" ? toggle() : null;
                        }}
                    >
                        <Dropdown height={22} width={30} />
                    </span>
                    <button
                        type="button"
                        class="btn fw-normal btn-primary ms-3 h-100 d-flex justify-content-center align-items-center " on:click={()=>{$selected_submit=selected}}
                        >Anzeigen</button
                    >
                </div>

                <div
                    class="dropdown-menu {show}"
                    aria-labelledby="dropdownMenuLink"
                >
                    <span
                        class="dropdown-item"
                        on:click={() => {
                            (selected = null), (show = "");
                        }}>Alle</span
                    >
                    <span
                        class="dropdown-item"
                        on:click={() => {
                            (selected = "test"), (show = "");
                        }}>Test</span
                    >
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
