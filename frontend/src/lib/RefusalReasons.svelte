<script>
    import Card from "./Card.svelte";
    import { stats } from "../stores/stats.js";
    import { formatAsPercent, formatCosts } from "./helpers/formatting";
</script>

<Card title={"Warum lehnt der Staat Anfragen ab?"}>
    <ul>
        <li class="mb-3">
            <span class="h5">{formatAsPercent($stats.other_or_no_reason)}</span>
            der abgelehnten Anfragen fehlt ein Ablehnungsgrund oder es liegt ein
            anderer, unbekannter Grund vor.
        </li>
        <li class="mb-3">
            <span class="h5"
                >{formatAsPercent($stats.refusal_reasons_specified)}</span
            > der abgelehnten Anfragen wurden begründet.
        </li>

        <li class="mb-5">
            <span class="h5">{formatAsPercent($stats.no_law_applicable)}</span> der
            abgelehnten Anfragen wurden abgelehnt, weil das angegebene Gesetz nicht
            anwendbar ist.
        </li>
    </ul>
    <h5 class="mb-3">Häufigste Ablehnungsgründe:</h5>
    {#if $stats.refusal_reasons.length != 0}
        <table class="table">
            <thead class="bigger">
                <tr>
                    <th scope="row">#</th>
                    <th>Grund</th>
                    <th>Anzahl</th>
                </tr>
            </thead>
            <tbody>
                {#each $stats.refusal_reasons as item, i}
                    <tr>
                        <th>
                            {i+1}
                        </th>
                        <td>
                            {item.reason}
                        </td>
                        <td>
                            {item.count}
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {/if}
</Card>
