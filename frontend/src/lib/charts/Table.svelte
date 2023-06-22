<script>
  export let data;
  import { formatAsPercent } from "../helpers/formatting";



</script>

<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">Name</th>
      <th scope="col">Anfragen</th>
      <th scope="col">Verpätungsquote</th>
      <th scope="col">Erfolgreich</th>
      <th scope="col">Erfolgsquote</th>
    </tr>
  </thead>
  <tbody>
    {#each data as row,i}
    <tr>
      <th scope="row">{i+1}</th>
      <td>{row.name}</td>
      <td>{row.number}</td>
      <td>{formatAsPercent(row.overdue_rate)}</td>
      <td>{row.successful}</td>
      <td>{formatAsPercent(row.success_rate)}</td>
    </tr>
    {/each}   
  </tbody>
</table>
