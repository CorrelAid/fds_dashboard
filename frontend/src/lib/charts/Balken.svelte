<script>
    import * as echarts from "echarts";
    import { onMount, onDestroy } from "svelte";

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

    let el;
    let notMerge = false;
    let replaceMerge = undefined;
    let lazyUpdate = false;

    var option = {
        animation: false,
        legend: {},
        grid: { left: "0%", bottom: "0%", right: "0%", top: "0%" },
        dataset: {
            // Provide a set of data.
            dimensions: ["value", "name"],
            source: data,
        },
        tooltip:{},
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
