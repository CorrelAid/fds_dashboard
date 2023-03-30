<script>
    import * as echarts from "echarts";
    import { onMount, onDestroy } from "svelte";

    export let data;
    export let height;

    $: console.log(data)

    let el;
    let notMerge = false;
    let replaceMerge = undefined;
    let lazyUpdate = false;

    var option = {
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
                markPoint: {
                    data: [
                        {
                            type: "max",
                            show: true,
                            symbol: "circle",
                            symbolSize: 10,
                            label:{
                                position: "top",
                                fontStyle: "bold",
                                fontSize: "16"
                            }
                            
                        },
                    ],
                },
            },
        ],
    };

    let chart; // our chart instance

    const setOption = () => {
        if (chart && !chart.isDisposed()) {
            chart.setOption(option, notMerge, replaceMerge, lazyUpdate);
        }
    };

    const destroyChart = () => {
        if (chart && !chart.isDisposed()) {
            chart.dispose();
        }
    };

    const makeChart = () => {
        destroyChart();
        chart = echarts.init(el);
        setOption();
    };

    onMount(() => {
        makeChart();
    });

    onDestroy(() => {
        destroyChart();
    });
</script>

<svelte:window on:resize={makeChart} />

<div bind:this={el} class="w-100" style="height: {height}px" />
