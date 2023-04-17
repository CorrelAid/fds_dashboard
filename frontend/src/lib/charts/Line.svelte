<script>
    import * as echarts from "echarts";
    import { onMount, onDestroy } from "svelte";

    export let data;
    export let height;
    export let y_labels = [];

    let el;
    let notMerge = false;
    let replaceMerge = undefined;
    let lazyUpdate = false;

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

    let chart; // our chart instance

    const setOption = (options) => {
        if (chart && !chart.isDisposed()) {
            chart.setOption(options, notMerge, replaceMerge, lazyUpdate);
        }
    };

    const destroyChart = () => {
        if (chart && !chart.isDisposed()) {
            chart.dispose();
        }
    };

    const makeChart = (el,options) => {
        destroyChart();
        chart = echarts.init(el);
        setOption(options);
    };

    onMount(() => {
        makeChart(el,gen_options(data));
    });

    $: if (el) {
        console.log("change");
        makeChart(el,gen_options(data));
    }

    onDestroy(() => {
        destroyChart();
    });
</script>

<svelte:window on:resize={makeChart(el,gen_options(data))} />

{#if y_labels != []}
    <div bind:this={el} class="w-100" style="height: {height}px" />
{/if}
