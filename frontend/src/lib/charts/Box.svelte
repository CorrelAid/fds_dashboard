<script>
    import Chart from "./Chart.svelte";
    import { roundNumber } from "../helpers/formatting";

    const colorPalette = [
        "#0047e1",
        "#FE4A49",
        "#FBD766",
        "#61E294",
        "#B6DDF5",
        "#FDE9AE",
    ];
    let data_
    export let unit;
    export let name;
    export let data;
    export let decimal_Places;
    $: if (data) {
        data_ = [
            [
                data.Min.value,
                data.Median,
                data.Median,
                data.Median,
                data.Max.value,
            ],
        ];
    }
    let average = data.Average;
    export let height;


    const gen_options = (data_) => {
        return {
            animation: false,
            tooltip: {
                trigger: "axis",
                show: true,
                formatter: `Minimale ${name}: <strong>${roundNumber(data_[0][0], decimal_Places)}</strong> ${unit} <br/> 
                Median ${name}: <strong>${roundNumber(data_[0][2], decimal_Places)}</strong> ${unit} <br/>
                Durchschnittliche ${name}: <strong>${roundNumber(average, 2)}</strong> ${unit} <br/>
                Maximale ${name}: <strong>${roundNumber(data_[0][4], decimal_Places)}</strong> ${unit}`,
            },
            yAxis: {
                type: "category",
                show: false,
            },
            xAxis: {
                type: "value",
                show: true,
                min: 0,
                name: `${name} in ${unit}`,
                nameLocation: "center",
                nameGap: 35,
                nameTextStyle: {
                    fontSize: 13,
                },
            },
            grid: { left: "15%", bottom: "27%", right: "19%", top: "5%" },
            series: [
                {
                    type: "boxplot",
                    layout: "horizontal",
                    data: data_,
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
                                    formatter: `${roundNumber(data.Min.value, decimal_Places)}`,
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
                                    formatter: `${roundNumber(data.Max.value, decimal_Places)}`,
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
                                    formatter: `${roundNumber(data.Median, decimal_Places)}`,
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

{#if data_}
    <Chart options={gen_options(data_)} {height} />
{/if}
