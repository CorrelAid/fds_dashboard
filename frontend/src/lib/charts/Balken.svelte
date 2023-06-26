<script>
    import Chart from "./Chart.svelte";

    const colorPalette = [
        "#fd7f6f",
        "#7eb0d5",
        "#b2e061",
        "#bd7ebe",
        "#ffb55a",
        "#ffee65",
        "#beb9db",
        "#fdcce5",
        "#8bd3c7",
    ];

    export let data;
    export let height;


    const gen_options = (data) => {
        return {
            animation: false,
            legend: {},
            grid: { left: "0%", bottom: "0%", right: "0%", top: "0%" },
            dataset: {
                // Provide a set of data.
                dimensions: ["value", "name"],
                source: data,
            },
            tooltip: {},
            xAxis: {
                type: "value",
                logBase: 12,
                boundaryGap: [0, 0.01],
            },
            yAxis: {
                type: "category",
            },
            series: [
                {
                    type: "bar",
                    barWidth: "75%",
                    encode: {
                        y: "name",
                        x: "value",
                        tooltip: ["value"],
                    },
                },
            ],
        };
    };
</script>

{#if data}
    <Chart options={gen_options(data)} {height} />
{/if}
