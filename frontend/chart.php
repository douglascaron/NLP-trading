<html>
<head>
  <script src="assets/base.min.js"></script>
  <script src="assets/ui.min.js"></script>
  <script src="assets/exports.min.js"></script>
  <script src="assets/stock.min.js"></script>
  <script src="assets/data-adapter.min.js"></script>
  <link href="assets/ui.min.css" type="text/css" rel="stylesheet">
  <link href="assets/font.min.css" type="text/css" rel="stylesheet">
  <style type="text/css">

    html,
    body,
    #container {
      width: 100%;
      height: 100%;
      margin: 0;
      padding: 0;
    }
  
</style>
</head>
<body>
  
  <div id="container"></div>
  

  <script>

    anychart.onDocumentReady(function () {
      anychart.data.loadCsvFile(
        'market_data.csv',
        function (data) {
          var dataTable = anychart.data.table();
          dataTable.addData(data);

          var mapping = dataTable.mapAs({
            open: 1,
            high: 2,
            low: 3,
            close: 4
          });

          // map loaded data for the scroller
          var scrollerMapping = dataTable.mapAs();
          scrollerMapping.addField('value', 5);

          // create stock chart
          var chart = anychart.stock();

          // create first plot on the chart
          var plot = chart.plot(0);
          // set grid settings
          plot.yGrid(true).xGrid(true).yMinorGrid(true).xMinorGrid(true);

          // create EMA indicators with period 50
          plot
            .ema(dataTable.mapAs({ value: 4 }))
            .series()
            .stroke('1.5 #455a64');

          // create ohlc series
          plot
            .ohlc()
            .data(mapping)
            .name('Market Data')
            .legendItem({ iconType: 'rising-falling' });

          // create scroller series with mapped data
          chart.scroller().ohlc(mapping);

          // set container id for the chart
          chart.container('container');
          // initiate chart drawing
          chart.draw();

          // create range picker
          var rangePicker = anychart.ui.rangePicker();
          // init range picker
          rangePicker.render(chart);

          // create range selector
          var rangeSelector = anychart.ui.rangeSelector();
          // init range selector
          rangeSelector.render(chart);
        }
      );
    });
  
</script>
</body>
</html>