<script>
    import Chart from "./Chart.svelte";
    export let data;
    export let height;
    export let x_labels = [];
    import { formatGermanDate } from "../helpers/formatting";

    const gen_options = (data) => {
        return {
            animation: false,
            legend: {},
            tooltip: {
                trigger: "axis",
                formatter: function (params) {
                    params = params[0].data;
                    var date = new Date(params.name);
                    return `${formatGermanDate(date)}: <strong>${params.value}</strong>`;
                },
            },
            grid: { left: "5%", bottom: "10%", right: "8%", top: "10%" },
            color: ["#3f52d4"],
            dataset: {
                // Provide a set of data.
                dimensions: ["value", "name"],
                source: data,
            },
            xAxis: { type: "time" },
            yAxis: { type: "value" },
            series: [
                {
                    type: "line",
                    showSymbol: false,
                    encode: {
                        x: "name",
                        y: "value",
                        tooltip: ["value"],
                    },
                    markLine: {
                        silent: false,

                        symbol: "none",
                        lineStyle: {
                            color: "#333",
                            type: "solid",
                        },
                        emphasis: {
                            label: {
                                show: true,
                                formatter: "{b}",
                            },
                        },
                        label: {
                            show: false,
                            formatter: "{b}",
                        },
                        data: x_labels,
                    },
                    markPoint: {
                        data: [
                            {
                                type: "max",
                                show: true,
                                symbol: "circle",
                                symbolSize: 10,
                                label: {
                                    position: "right",
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 20
                                },
                                
                                   
                                
                            },
                        ],
                    },
                },
            ],
        };
    };
</script>

{#if x_labels}
    <Chart options={gen_options(data)} {height} />
{/if}
