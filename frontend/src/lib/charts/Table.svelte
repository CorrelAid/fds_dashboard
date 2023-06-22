<script>
  export let data;
  import { formatAsPercent } from "../helpers/formatting";
  import { values_campaigns } from "../../stores/ranking_campaigns";
  import ArrowDown from "../svg/ArrowDown.svelte";
  import ArrowUp from "../svg/ArrowUp.svelte";

  export let values = {
    Anzahl: { ascending: false, selected: true },
    Verspätungsquote: { ascending: true, selected: false },
    Erfolgreich: { ascending: true, selected: false },
    Erfolgsquote: { ascending: true, selected: false },
  };

  const ar_cols ={
    Anzahl: { arrow_col: "arrow-white" },
    Verspätungsquote:  { arrow_col: "arrow-blue" },
    Erfolgreich:  { arrow_col: "arrow-blue" },
    Erfolgsquote: { arrow_col: "arrow-blue" },
  }

  const arrow_size = 20;

  const th = [
    { name: "#" },
    { name: "Name" },
    { name: "Anzahl", descending_only: true },
    { name: "Verspätungsquote" },
    { name: "Erfolgreich" },
    { name: "Erfolgsquote" },
  ];

  

  function handleClick(name,item) {
    if (item.descending_only !== true){
    values[name].ascending === true && values[name].selected === true
      ? (values[name].ascending = false)
      : (values[name].ascending = true);
    }
    // only change selecred when
    if (values[name].selected !== true){
    values[name].selected = true;
    ar_cols[name].arrow_col = "arrow-white"

    for (const key in values) {
      if (key != name) {
        values[key].selected = false;
        ar_cols[key].arrow_col = "arrow-blue"
        console.log("Hu")
      }
    }}
  }
function handleHover(name, enter){
  
  if(values[name].selected !== true){
   
  enter === true ? ar_cols[name].arrow_col = "arrow-white" : ar_cols[name].arrow_col = "arrow-blue"
  }
  
}

</script>

<table class="table">
  <thead >
    <tr >
      {#each th as item}
        <th scope="col"
          ><span class="">
            {#if values[item.name]}
              <button
                class="{ar_cols[item.name].arrow_col} d-flex align-items-center btn {values[item.name]
                  .selected === true
                  ? 'btn-primary'
                  : 'btn-outline-primary'} " 
                on:click={() => handleClick(item.name,item)}
                on:mouseover={() => handleHover(item.name, true)} on:mouseout={() => handleHover(item.name, false)}
                on:focus={() => handleHover(item.name, true)} on:blur={() => handleHover(item.name, false)}
              >
                {item.name}
                {#if values[item.name].ascending === false | item.descending_only === true}
                  <span class="mb-1 arrow"
                    ><ArrowDown width={arrow_size} height={arrow_size} /></span
                  >{/if}

                {#if values[item.name].ascending === true}
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
        <td>{row.name}</td>
        <td>{row.number}</td>
        <td>{formatAsPercent(row.overdue_rate)}</td>
        <td>{row.successful}</td>
        <td>{formatAsPercent(row.success_rate)}</td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  
</style>
