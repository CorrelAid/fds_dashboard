<script>
    import Chart from "./Chart.svelte";
    export let data;
    export let height;
    export let y_labels = [];


    $: console.log(data);

    let options;

    const gen_options = (data) => {
        return {
            animation: false,
            legend: {},
            tooltip: { trigger: "axis" },
            grid: { left: "15%", bottom: "10%", right: "10%", top: "10%" },
            color: ["#296dff"],
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
                        symbol: "none",
                        lineStyle: {
                            color: "#333",
                            type: "solid",
                        },
                        label: {
                            show: true,
                            formatter: "{b}",
                        },
                        data: y_labels,
                    },
                    markPoint: {
                        data: [
                            {
                                type: "max",
                                show: true,
                                symbol: "circle",
                                symbolSize: 10,
                                label: {
                                    position: "top",
                                    fontStyle: "bold",
                                    fontSize: "16",
                                },
                            },
                        ],
                    },
                },
            ],
        };
    };

</script>

<Chart options={gen_options(data)} {height} />
