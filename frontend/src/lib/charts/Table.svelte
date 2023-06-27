<script>
  export let data;
  import { formatAsPercent, roundNumber } from "../helpers/formatting";
  import ArrowDown from "../svg/ArrowDown.svelte";
  import ArrowUp from "../svg/ArrowUp.svelte";
  import { general_info, term } from "../../stores/general_info.js";
  import { set_url_params } from "../helpers/urlOps";
  import { url_params } from "../../stores/stats.js";

  export let values = {
    Anzahl: { ascending: false, selected: true },
    Verspätungsquote: { ascending: true, selected: false },
    Erfolgsquote: { ascending: true, selected: false },
    Kosten: { ascending: true, selected: false },
    Dauer: { ascending: true, selected: false },
  };

  export let type;

  const ar_cols = {
    Anzahl: { arrow_col: "arrow-white" },
    Verspätungsquote: { arrow_col: "arrow-blue" },
    Erfolgsquote: { arrow_col: "arrow-blue" },
    Dauer: { arrow_col: "arrow-blue" },
    Kosten: { arrow_col: "arrow-blue" },
  };

  const arrow_size = 20;

  const th = [
    { key: "",name: "#" },
    { key: "", name: "Name" },
    { key: "Anzahl", name: "Anzahl", descending_only: true },
    { key: "Verspätungsquote", name: "Verspätet" },
    { key: "Erfolgsquote", name: "Erfolgreich" },
    { key: "Dauer", name: "Ø-Dauer" },
    { key: "Kosten", name: "Ø-Kosten" },
  ];

  function handleClick(name, item) {
    if (item.descending_only !== true) {
      values[name].ascending === true && values[name].selected === true
        ? (values[name].ascending = false)
        : (values[name].ascending = true);
    }
    // only change selecred when
    if (values[name].selected !== true) {
      values[name].selected = true;
      ar_cols[name].arrow_col = "arrow-white";

      for (const key in values) {
        if (key != name) {
          values[key].selected = false;
          ar_cols[key].arrow_col = "arrow-blue";
        }
      }
    }
  }
  function handleHover(name, enter) {
    if (values[name].selected !== true) {
      enter === true
        ? (ar_cols[name].arrow_col = "arrow-white")
        : (ar_cols[name].arrow_col = "arrow-blue");
    }
  }

  function getid(name) {
    const temp = $general_info[type].find((obj) => obj.name === name).id;

    return temp;
  }
  function handleLinkClick(name) {
    const id = getid(name);
    $url_params = set_url_params(id, type);
    $term = name;
  }
</script>

{#if $general_info.jurisdictions}
  <table class="table">
    <thead class="bigger">
      <tr>
        {#each th as item}
          <th scope="col"
            ><span class="">
              {#if values[item.key]}
                <button
                  class="{ar_cols[item.key]
                    .arrow_col} d-flex align-items-center btn {values[item.key]
                    .selected === true
                    ? 'btn-primary'
                    : 'btn-outline-primary'} "
                  on:click={() => handleClick(item.key, item)}
                  on:mouseover={() => handleHover(item.key, true)}
                  on:mouseout={() => handleHover(item.key, false)}
                  on:focus={() => handleHover(item.key, true)}
                  on:blur={() => handleHover(item.key, false)}
                >
                  {item.name}
                  {#if (values[item.key].ascending === false) | (item.descending_only === true)}
                    <span class="mb-1 arrow"
                      ><ArrowDown
                        width={arrow_size}
                        height={arrow_size}
                      /></span
                    >{/if}

                  {#if values[item.key].ascending === true}
                    <span class="mb-1 arrow"
                      ><ArrowUp width={arrow_size} height={arrow_size} /></span
                    >
                  {/if}
                </button>
              {:else}
                {item.name}
              {/if}
            </span></th
          >
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each data as row, i}
        <tr>
          <th scope="row">{i + 1}</th>
          <td
            ><a href="#top" on:click={() => handleLinkClick(row.name)}
              >{row.name}</a
            ></td
          >
          <td>{row.number}</td>
          <td>{formatAsPercent(row.overdue_rate)}</td>
          <td>{formatAsPercent(row.success_rate)}</td>
          <td>{roundNumber(row.avg_time, 0)} Tage</td>
          <td>{roundNumber(row.avg_cost, 2)}€</td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}

<style>
  .bigger tr th {
    padding-bottom: 20px !important;
  }
</style>
