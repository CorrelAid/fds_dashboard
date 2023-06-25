<script>
    import * as echarts from "echarts";
    import { onMount, onDestroy } from "svelte";

    export let height;
    export let options;

    let el;
    let notMerge = false;
    let replaceMerge = undefined;
    let lazyUpdate = false;

    

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
        makeChart(el,options);
    });

    $: if (el) {
        makeChart(el,options);
    }

    onDestroy(() => {
        destroyChart();
    });
</script>

<svelte:window on:resize={makeChart(el,options)} />

<div bind:this={el} class="w-100" style="height: {height}px" />
