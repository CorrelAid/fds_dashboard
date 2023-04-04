<script>
  export let data;
  import { formatAsPercent } from "../helpers/formatting";

  // $: console.log(data)


</script>

<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
      <th scope="col">Anfragen</th>
      <th scope="col">Erfolgsquote</th>
      <th scope="col">Verspätet</th>
    </tr>
  </thead>
  <tbody>
    {#each data.public_bodies as row,i}
    <tr>
      <th scope="row">{i+1}</th>
      <td>{row.name}</td>
      <td>{row.number}</td>
      <td>{formatAsPercent(row.success_rate)}</td>
      <td>{formatAsPercent(row.overdue_rate)}</td>
    </tr>
    {/each}   
  </tbody>
</table>
