<script>
    import * as echarts from "echarts";
    import { onMount, onDestroy } from "svelte";

    export let data;
    export let height;

    let el;
    let notMerge = false;
    let replaceMerge = undefined;
    let lazyUpdate = false;

    var option = {
        animation: false,
        tooltip: {
            trigger: "item",
        },
        legend: {
            bottom: "0%",
            left: "center",
        },
        dataset: {
                    // Provide a set of data.
                    dimensions: ["value", "name"],
                    source: data,
                },
        series: [
            {   
                top: '-10%',
                left: '-10%',
                right: '-10%',
                bottom: '5%',
                type: "pie",
                radius: ["40%", "70%"],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: "center",
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 40,
                        fontWeight: "bold",
                    },
                },
                labelLine: {
                    show: false,
                }
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
