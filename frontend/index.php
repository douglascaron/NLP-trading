<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Data Dashboard</title>
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        .dashboard-container {
            position: relative;
            width: 100vw;
            height: 100vh;
        }

        .dashboard-section {
            position: absolute;
            width: 50%;
            height: 50%;
            overflow: hidden;
        }

        #top-left { top: 0; left: 0; }
        #top-right { top: 0; left: 50%; }
        #bottom-left { top: 50%; left: 0; }
        #bottom-right { top: 50%; left: 50%; }

        .chart-iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>

<body>

    <div class="dashboard-container">

        <div id="top-left" class="dashboard-section">
            <iframe src="chart.php" class="chart-iframe"></iframe>
        </div>

        <div id="top-right" class="dashboard-section">
            <iframe src="chart.php" class="chart-iframe"></iframe>
        </div>

        <div id="bottom-left" class="dashboard-section">
            <iframe src="chart.php" class="chart-iframe"></iframe>
        </div>

        <div id="bottom-right" class="dashboard-section">
            <iframe src="chart.php" class="chart-iframe"></iframe>
        </div>

    </div>

</body>

</html>
