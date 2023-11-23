<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Chart</title>
    <!-- Load Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Canvas to draw the chart -->
    <canvas id="stockChart" width="800" height="400"></canvas>

    <!-- PHP code to get the data from the CSV file -->
    <?php
        $csvFile = 'market_data.csv';
        $data = array_map('str_getcsv', file($csvFile));
        $header = array_shift($data); // Remove header row

        $dates = [];
        $closePrices = [];

        foreach ($data as $row) {
            $dates[] = $row[0]; // Assuming the first column is the date
            $closePrices[] = $row[3]; // Assuming the fourth column is the closing price
        }
    ?>

    <!-- JavaScript code to create the chart -->
    <script>
        var ctx = document.getElementById('stockChart').getContext('2d');
        var stockChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: <?php echo json_encode($dates); ?>,
                datasets: [{
                    label: 'Closing Prices',
                    data: <?php echo json_encode($closePrices); ?>,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    }
                }
            }
        });
    </script>
</body>
</html>
