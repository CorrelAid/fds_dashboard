<script>
    import Chart from "./Chart.svelte";
    import { formatAsPercent, formatCosts } from "../helpers/formatting";

    const colorPalette = [
        "#0047e1",
        "#FE4A49",
        "#FBD766",
        "#61E294",
        "#B6DDF5",
        "#FDE9AE",
    ];

    export let data;
    export let height;
    export let centerNumber = undefined;

    $: sum = data.reduce((total, item) => total + item.value, 0);

    const gen_options = (data) => {
        return {
            animation: false,
            tooltip: {
                trigger: "item",
                formatter: function (params) {
                    params = params.data;
                    return `${params.name}: <strong>${params.value}</strong>`;
                },
            },
            dataset: {
                // Provide a set of data.
                dimensions: ["value", "name"],
                source: data,
            },
            title: {
                text: `Insg. ${centerNumber}`,
                show: true,
                right: "center",
                top: "center",
                textStyle:{
                    width: 180,
                overflow: "break",
                },
               

            },
            series: [
                {
                    color: colorPalette,
                    type: "pie",
                    // left: "-40%",
                    radius: ["55%", "78%"],
                    overflow: "breakAll",

                    avoidLabelOverlap: true,
                    label: {
                        show: true,
                        formatter: function (params) {
                            const data = params.data;
                            const value = data.value;
                            const name = data.name;
                            const perc = formatAsPercent(
                                (value / sum) * 100,
                                1
                            );
                            return `{a|${perc}}{b| ${name}}`;
                        },
                        rich: {
                            a: {
                                fontStyle: "bold",
                                fontSize: 16,
                                color: "#001c5a",
                            },
                            b: {
                                fontSize: 13,
                                color: "#001c5a",
                            },
                        },
                        overflow: "break",
                    },
                    labelLayout: {
                        moveOverlap: "shiftY",
                    },

                    labelLine: {
                        show: true,
                        lineStyle: {
                            color: "#001c5a",
                        },
                    },
                },
            ],
        };
    };
</script>

<Chart options={gen_options(data)} {height} />
