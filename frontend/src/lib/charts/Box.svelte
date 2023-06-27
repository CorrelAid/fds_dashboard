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

    export let data = [[655, 940, 940, 940, 1175]];
    export let average = 950
    export let height;

    $: console.log(data);

    const gen_options = (data) => {
        return {
            animation: false,
            tooltip: {
                trigger: "axis",
                show: true,
                formatter: `Schnellste Abschlussdauer: <strong>${data[0][0]}</strong> Tage <br/> 
                Median Abschlussdauer: <strong>${data[0][2]}</strong> Tage <br/>
                Durchschnittliche Abschlussdauer: <strong>${average}</strong> Tage <br/>
                Langsamste Abschlussdauer: <strong>${data[0][4]}</strong> Tage`,
            },
            yAxis: {
                type: "category",
                show: false,
            },
            xAxis: {
                type: "value",
                show: true,
                min: function (value) {
                    return value.min - 20;
                },
                name: "Abschlussdauer in Tagen",
                nameLocation: "center",
                nameGap: 35,
                nameTextStyle: {
                    fontSize: 13,
                },
            },
            grid: { left: "15%", bottom: "27%", right: "15%", top: "5%" },
            series: [
                {
                    type: "boxplot",
                    layout: "horizontal",
                    data: data,
                    dimensions: ["minimum", null, "median", null, "maximum"],
                    color: "#0047e1",
                    boxWidth: ["10%", "28%"],
                    itemStyle: {
                        borderType: "solid",
                        borderWidth: 3,
                        borderCap: "round",
                    },
                    silent: false,
                    markPoint: {
                        data: [
                            {
                                name: "minimum",
                                type: "min",
                                show: true,
                                symbol: "circle",
                                symbolSize: 0,
                                label: {
                                    position: "left",
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 20,
                                    distance: 8,
                                    width: 100,
                                    overflow: "break",
                                },
                            },
                            {
                                valueIndex: 5,
                                type: "max",
                                show: true,
                                symbol: "circle",
                                symbolSize: 0,
                                label: {
                                    position: "right",
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 20,
                                    distance: 10,
                                },
                            },
                            {
                                valueIndex: 2,
                                type: "max",
                                show: true,
                                symbol: "circle",
                                symbolSize: 0,
                                label: {
                                    position: "top",
                                    distance: 25,
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 20,
                                },
                            },
                            {
                                valueIndex: 2,
                                type: "max",
                                show: true,
                                symbol: "circle",
                                symbolSize: 0,
                                label: {
                                    position: "top",
                                    distance: 25,
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 20,
                                },
                            },
                            {
                                name: "fixed x position",
                                yAxis: 0,
                                xAxis: average,
                                show: true,
                                symbol: "circle",
                                symbolSize: 12,
                                // value: average,
                                label: {
                                    position: "bottom",
                                    distance: 15,
                                    fontStyle: "bold",
                                    fontFamilty: "inherit",
                                    fontSize: "16",
                                    color: "#001c5a",
                                    fontSize: 16,
                                },
                            },
                        ],
                    },
                },
            ],
        };
    };
</script>

{#if data}
    <Chart options={gen_options(data)} {height} />
{/if}
