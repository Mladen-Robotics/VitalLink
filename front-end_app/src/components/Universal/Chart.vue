<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
    props: ['id'],
    data() {
      return {
          xData: [],
          yData: [],
          chart: null, // Store the chart instance
      };
    },
    methods: {
        async getChartData() {
            let timeTempResponse;
            let bpmResponse;
            // Getting the time
            try {
                timeTempResponse = await axios.get(`http://localhost:5000/patient/${this.id}/temp`, {withCredentials: true});
                timeTempResponse = timeTempResponse.data;
            } catch(error) {
                console.error("Chart data couldn't be loaded: " + error);
            }
            
            let timeArray = this.formatTime(timeTempResponse);
            
            // Getting the temperature
            let tempArray = this.formatValue(timeTempResponse);
        
            // Getting the BPM
            try {
                bpmResponse = await axios.get(`http://localhost:5000/patient/${this.id}/bpm`, {withCredentials: true});
                bpmResponse = bpmResponse.data;
            } catch(error) {
                console.error("Chart data couldn't be loaded: " + error);
            }
            let bpmArray = this.formatValue(bpmResponse);

            // Update data
            this.xData = timeArray;
            this.yData = [tempArray, bpmArray];
            
            // Update chart if it exists
            if (this.chart) {
                this.updateChart();
            } else {
                this.createChart();
            }
        },
        formatTime(response) {
            let output = [];
            for(let i=0; i < Object.keys(response).length; i++) {
                const rawTime = response[i].time;
                const timeObject = new Date(rawTime);
                const time = `${timeObject.getMinutes()}:${timeObject.getSeconds()}`;
                output.push(time);
            }
            return output;
        },
        formatValue(response) {
            // Formats anything other than time (everything that is accessed with the value key)
            let output = [];
            for(let i=0; i < Object.keys(response).length; i++) {
                output.push(response[i].value)
            }
            return output;
        },
        updateChart() {
            // Update just the series data without recreating the chart
            this.chart.updateOptions({
                xaxis: {
                    categories: this.xData
                }
            });
            
            this.chart.updateSeries([
                {
                    name: 'Температура',
                    data: this.yData[0]
                },
                {
                    name: 'Пулс',
                    data: this.yData[1]
                }
            ]);
        },
        createChart() {
            var options = {
                chart: {
                    type: 'line',
                    height: 350,
                    animations: {
                        enabled: false,
                        speed: 200,
                        animateGradually: {
                            enabled: true,
                            delay: 150
                        },
                        dynamicAnimation: {
                            enabled: true,
                            speed: 350
                        }
                    }
                },
                dataLabels: {
                    enabled: true
                },
                series: [
                    {
                        name: 'Температура',
                        data: this.yData[0] || []
                    },
                    {
                        name: 'Пулс',
                        data: this.yData[1] || []
                    }
                ],
                xaxis: {
                    categories: this.xData,
                    axisBorder: {
                        show: true,
                        color: '#000',
                        height: 2
                    },
                    axisTicks: {
                        show: true,
                        color: '#000',
                        height: 6
                    },
                    labels: {
                        style: {
                            fontWeight: 'bold',
                        },
                        offsetY: 8,
                    }
                },
                yaxis: {
                    min: 25,
                    max: 50,
                    axisBorder: {
                        show: true,
                        color: '#000',
                        width: 2
                    },
                    axisTicks: {
                        show: true,
                        color: '#000',
                        width: 6
                    },
                    labels: {
                        style: {
                            fontWeight: 'bold',
                        }
                    }
                },
                grid: {
                    show: true,
                    xaxis: {
                        lines: {
                            show: true,
                        },
                    },
                    yaxis: {
                        lines: {
                            show: false,
                        },
                    },
                    borderColor: '#90A4AE',
                    strokeDashArray: 7,
                    position: 'back',
                },
                legend: {
                    show: true,
                    position: 'top',
                    onItemHover: {
                        highlightDataSeries: true
                    }
                },
                noData: {
                    text: "Loading...",
                    align: 'center',
                    verticalAlign: 'middle',
                }
            };

            // Create chart and store the instance
            this.chart = new ApexCharts(document.querySelector(`#chart${this.id}`), options);
            this.chart.render();
        }
    },
    mounted() {
        this.getChartData();
        setInterval(() => {
            this.getChartData();
        }, 2000);
    },
    beforeUnmount() {
        // Clean up the chart when the component is destroyed
        if (this.chart) {
            this.chart.destroy();
        }
    }
};
</script>

<template>
    <div :id="'chart' + id" class="chart"></div>
</template>

<style scoped>
.chart {
    width: 100%;
    height: 300px; /* Adjust height as needed */
}
</style>