<script>
    import Chart from "./Chart.svelte";

    export let data;
    export let height;

    const gen_options = (data) => {
        return {
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
                    top: "-10%",
                    left: "-10%",
                    right: "-10%",
                    bottom: "5%",
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
                    },
                },
            ],
        };
    };
</script>

<Chart options={gen_options(data)} {height} />
