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


    $: if (data) {
        const nameColors = {
            Erfolgreich: "#0047e1",
            Zurückgezogen: "#FBD766",
            Abgelehnt: "#FE4A49",
            "Information nicht vorhanden": "#B6DDF5",
            "Teilweise erfolgreich": "#61E294",
            Unbekannt: "#FDE9AE",
        };
        for (let i = 0; i < data.length; i++) {
            const name = data[i].name;
            const color = nameColors[name];
            data[i].itemStyle = {};
            data[i].itemStyle.color = color;
        }
    }

    $: console.log(data);

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
            // dataset: {
            //     // Provide a set of data.
            //     dimensions: ["value", "name"],
            //     source: data,
            // },
            title: {
                text: `Abgeschlossen: ${centerNumber}`,
                show: true,
                right: "center",
                top: "center",
                textStyle: {
                    width: 180,
                    overflow: "break",
                },
            },
            series: [
                {
                    type: "pie",
                    data : data,
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

{#if data}
    <Chart options={gen_options(data)} {height} />
{/if}
