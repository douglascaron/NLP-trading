<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Data Chart</title>
    <script type="text/javascript" src="https://unpkg.com/lightweight-charts@4.1.1/dist/lightweight-charts.standalone.production.js"></script>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: linear-gradient(to bottom, #00030a, #0a0b1e);
            color: #d1d4dc;
        }

        #settings-window {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid #39424e;
        }

        #tradingview-menu {
            display: flex;
            flex-direction: row;
            gap: 10px;
            align-items: center;
        }

        #tradingview-menu select, button {
            margin-bottom: 0;
        }

        #chart-container {
            width: 100%;
            height: 100%;
            margin: 0px 0 0 0;
        }

        #stock-select.closed option:first-child {
            display: block;
        }

        label {
            margin-bottom: 5px;
        }

        select, button {
            margin-bottom: 10px;
            padding: 8px;
            font-size: 14px;
            border: 1px solid #39424e;
            border-radius: 4px;
            background-color: #222831;
            color: #d1d4dc;
            cursor: pointer;
            transition: background-color 0.3s, border-color 0.3s;
        }

        select:hover, button:hover {
            background-color: #39424e;
            border-color: #4b5563;
        }

        select, button {
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
            outline: none;
            border: 1px solid transparent;
            background-color: #222831;
            color: #d1d4dc;
            cursor: pointer;
            padding: 8px;
            font-size: 14px;
            border-radius: 4px;
            transition: background-color 0.3s, border-color 0.3s;
        }

        select::-ms-expand, button::-ms-expand {
            display: none;
        }


        #settings-window {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 300px;
            padding: 20px;
            background: #39424e;
            border: 1px solid #4b5563;
            border-radius: 5px;
            z-index: 999;
        }

        #settings-window .settings-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #d1d4dc;
        }

        #settings-window .close-button {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            color: #d1d4dc;
            padding: 8px;
            font-size: 14px;
            border: 1px solid #4b5563;
            border-radius: 4px;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s;
        }

        #settings-window .close-button:hover {
            background-color: #4b5563;
            border-color: #39424e;
            color: #fff;
        }



    </style>
</head>
<body style="margin: 0; padding: 0; overflow: hidden; background: linear-gradient(to bottom, #00030a, #0a0b1e); color: #d1d4dc;">
    <div id="chart-info" style="position: absolute; top: 10px; left: 10px; font-size: 14px; color: #d1d4dc;"></div>

    <div id="settings-window">
        <div class="settings-header">Settings</div>
        <div class="close-button" onclick="toggleSettings()">X</div>
        <div id="tradingview-menu">
            <select id="stock-select">
                <option value="AAPL">Apple Inc.</option>
                <option value="MSFT">Microsoft Corporation</option>
                <option value="GOOG">Alphabet Inc.</option>
                <option value="AMZN">Amazon.com Inc.</option>
                <option value="NVDA">NVIDIA Corporation</option>
                <option value="META">Meta Platforms Inc.</option>
                <option value="TSLA">Tesla Inc.</option>
                <option value="LLY">Eli Lilly and Company</option>
                <option value="V">Visa Inc.</option>
                <option value="UNH">UnitedHealth Group Incorporated</option>
                <option value="JPM">JP Morgan Chase & Co.</option>
                <option value="XOM">Exxon Mobil Corporation</option>
                <option value="WMT">Walmart Inc.</option>
                <option value="AVGO">Broadcom Inc.</option>
                <option value="MA">Mastercard Incorporated</option>
                <option value="JNJ">Johnson & Johnson</option>
                <option value="PG">Procter & Gamble Company</option>
                <option value="ORCL">Oracle Corporation</option>
                <option value="HD">Home Depot Inc.</option>
                <option value="ADBE">Adobe Inc.</option>
                <option value="CVX">Chevron Corporation</option>
                <option value="MRK">Merck & Company Inc.</option>
                <option value="COST">Costco Wholesale Corporation</option>
                <option value="KO">Coca-Cola Company</option>
                <option value="ABBV">AbbVie Inc.</option>
                <option value="BAC">Bank of America Corporation</option>
                <option value="PEP">PepsiCo Inc.</option>
                <option value="CRM">Salesforce Inc.</option>
                <option value="ACN">Accenture plc</option>
                <option value="NFLX">Netflix Inc.</option>
            </select>

            <select id="interval-select">
                <option value="5m">5 Minutes</option>
                <option value="1h">1 Hour</option>
                <option value="1d">1 Day</option>
            </select>

        </div>
    </div>

    <div id="chart-container"></div>

    <script>
        let lineSeries;
        let areaSeries;

        function loadChartData() {
            const selectedStock = document.getElementById('stock-select').value;
            const selectedInterval = document.getElementById('interval-select').value;

            const dataUrl = `data/stock_data_${selectedStock}_${selectedInterval}.csv`;

            fetch(dataUrl)
                .then(response => response.text())
                .then(data => {
                    const rows = data.split('\n');
                    const header = rows[0].split(',');
                    const seriesData = [];

                    for (let i = 1; i < rows.length; i++) {
                        const values = rows[i].split(',');
                        const rowData = {};

                        for (let j = 0; j < header.length; j++) {
                            rowData[header[j]] = values[j];
                        }

                        if (rowData['Datetime'] || rowData['Date']) {
                            const dateString = rowData['Datetime'] || rowData['Date'];
                            const dateTime = new Date(dateString);

                            let timestamp;

                            if (selectedInterval === '5m') {
                                timestamp = dateTime.getTime() / 1000;
                            } 
                            else if (selectedInterval === '1h') {
                                timestamp = dateTime.getTime() / 1000;
                            } else if (selectedInterval === '1d') {
                                timestamp = new Date(dateTime.toISOString().split('T')[0]).getTime() / 1000;
                            }

                            seriesData.push({
                                time: timestamp,
                                value: parseFloat(rowData['Close']),
                            });
                        }
                    }

                    lineSeries.setData(seriesData);
                    areaSeries.setData(seriesData);
                })
                .catch(error => console.error('Error fetching market data:', error));
        }


        document.addEventListener('DOMContentLoaded', function () {
            const chart = LightweightCharts.createChart(document.getElementById('chart-container'), {
                width: window.innerWidth,
                height: window.innerHeight,
                layout: {
                    background: { color: '#080918' },
                    textColor: '#d1d4dc',
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

            lineSeries = chart.addLineSeries({
                color: '#2962ff',
                lineWidth: 2,
                base: 0,
            });

            areaSeries = chart.addAreaSeries({
                topColor: 'rgba(41, 98, 255, 0.5)',
                bottomColor: 'rgba(41, 98, 255, 0)',
                lineColor: '#2962ff',
                lineWidth: 2,
            });

            loadChartData();

            document.getElementById('stock-select').addEventListener('change', loadChartData);
            document.getElementById('interval-select').addEventListener('change', loadChartData);
        });
        



        function toggleSettings() {
            const settingsWindow = document.getElementById('settings-window');
            settingsWindow.style.display = settingsWindow.style.display === 'none' ? 'block' : 'none';
        }

        document.addEventListener('DOMContentLoaded', function () {

            document.addEventListener('keydown', function (event) {
                if (event.key === 'h') {
                    toggleSettings();
                }
            });

            document.getElementById('stock-select').addEventListener('change', loadChartData);
            document.getElementById('interval-select').addEventListener('change', loadChartData);
        });



    </script>
</body>
</html>