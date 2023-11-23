<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Data Chart</title>
    <script type="text/javascript" src="https://unpkg.com/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>
</head>
<body>
    <div id="chart-container" style="width: 100%; height: 500px;"></div>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            // Load market data from CSV
            fetch('market_data.csv')
                .then(response => response.text())
                .then(data => {
                    // Parse CSV data
                    const rows = data.split('\n');
                    const header = rows[0].split(',');
                    const seriesData = [];

                    for (let i = 1; i < rows.length; i++) {
                        const values = rows[i].split(',');
                        const rowData = {};

                        for (let j = 0; j < header.length; j++) {
                            rowData[header[j]] = values[j];
                        }

                        // Check if Datetime exists in rowData
                        if (rowData['Datetime']) {
                            // Parse datetime and adjust for time zone offset
                            const datetimeString = rowData['Datetime'];
                            const dateComponents = datetimeString.split(' ');
                            const dateString = dateComponents[0];
                            const timeString = dateComponents[1].split('-')[0];
                            const dateTime = new Date(`${dateString}T${timeString}`);
                            const offsetMinutes = parseInt(dateComponents[1].split('-')[1]) || 0;
                            const adjustedDateTime = new Date(dateTime.getTime() - offsetMinutes * 60000);

                            seriesData.push({
                                time: adjustedDateTime.getTime() / 1000,
                                value: parseFloat(rowData['Close']), // Use 'Close' as the value for the line chart
                            });
                        }
                    }

                    // Create a chart with custom options
                    const chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
                        width: window.innerWidth,
                        height: 500,
                        layout: {
                            backgroundColor: '#0a0b1e',
                        },
                        grid: {
                            vertLines: {
                                visible: false,
                            },
                            horzLines: {
                                visible: false,
                            },
                        },
                        crosshair: {
                            mode: LightweightCharts.CrosshairMode.Normal,
                        },
                        timeScale: {
                            timeVisible: true,
                            secondsVisible: false,
                        },
                        priceScale: {
                            mode: LightweightCharts.PriceScaleMode.Normal,
                            borderColor: '#2962ff',
                        },
                    });

                    // Add a line series
                    const lineSeries = chart.addLineSeries({
                        color: '#2962ff',
                        lineWidth: 2,
                        base: 0,
                    });

                    // Add the parsed market data to the chart
                    lineSeries.setData(seriesData);

                    // Add a color gradient below the line
                    const areaSeries = chart.addAreaSeries({
                        topColor: 'rgba(41, 98, 255, 0)', // 0% opacity at the top
                        bottomColor: 'rgba(41, 98, 255, 1)', // 100% opacity at the line
                        lineColor: '#2962ff',
                        lineWidth: 2,
                    });
                    areaSeries.setData(seriesData);
                })
                .catch(error => console.error('Error fetching market data:', error));
        });
    </script>
</body>
</html>
