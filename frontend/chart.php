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

                        // Log rowData to see what's being parsed
                        console.log('Row Data:', rowData);

                        // Check if Datetime exists in rowData
                        if (rowData['Datetime']) {
                            // Parse datetime and adjust for time zone offset
                            const datetimeString = rowData['Datetime'];
                            console.log('Datetime String:', datetimeString);

                            const dateComponents = datetimeString.split(' ');
                            const dateString = dateComponents[0];
                            const timeString = dateComponents[1].split('-')[0];
                            const dateTime = new Date(`${dateString}T${timeString}`);
                            const offsetMinutes = parseInt(dateComponents[1].split('-')[1]) || 0;
                            const adjustedDateTime = new Date(dateTime.getTime() - offsetMinutes * 60000);

                            seriesData.push({
                                time: adjustedDateTime.getTime() / 1000,
                                open: parseFloat(rowData['Open']),
                                high: parseFloat(rowData['High']),
                                low: parseFloat(rowData['Low']),
                                close: parseFloat(rowData['Close']),
                                volume: parseFloat(rowData['Volume'])
                            });
                        } else {
                            console.log('Datetime is undefined in the row data. Skipping this row.');
                        }
                    }

                    // Create a chart with custom options
                    const chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
                        width: window.innerWidth,
                        height: 500,
                        layout: {
                            backgroundColor: '#f5f5f5',
                        },
                        grid: {
                            vertLines: {
                                color: 'rgba(197, 203, 206, 0.5)',
                            },
                            horzLines: {
                                color: 'rgba(197, 203, 206, 0.5)',
                            },
                        },
                        crosshair: {
                            mode: LightweightCharts.CrosshairMode.Normal,
                        },
                        timeScale: {
                            timeVisible: true,
                            secondsVisible: false,
                        },
                    });

                    // Add a candlestick series
                    const candlestickSeries = chart.addCandlestickSeries();

                    // Add the parsed market data to the chart
                    candlestickSeries.setData(seriesData);
                })
                .catch(error => console.error('Error fetching market data:', error));
        });
    </script>
</body>
</html>
