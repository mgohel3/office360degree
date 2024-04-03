document.addEventListener("DOMContentLoaded", function() {

        var options = {
        series: [
          {
            name: 'Detractors',
            data: [44, 55, 41, 10, 25, 15, 35, 15, 05, 15, 45, 09],
            color: '#FF0000' // Red color for Detractors
          },
          {
            name: 'Passive',
            data: [53, 32, 33, 40, 15, 35, 45, 05, 25, 45, 15, 31],
            color: '#FFBF00' // Amber color for Passive
          },
          {
            name: 'Promoters',
            data: [12, 17, 50, 10, 25, 35, 55, 05, 35, 25, 45, 65],
            color: '#00D100' // Green color for Promoters
          }
        ],
        chart: {
          type: 'bar',
          height: 350,
          stacked: true,
          stackType: '100%',
          toolbar: {
            show: false
          }
        },
        plotOptions: {
          bar: {
            horizontal: true,
          },
        },
        stroke: {
          width: 1,
          colors: ['#fff']
        },
        xaxis: {
          categories: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          labels: {
            show: false
          }
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return val.toFixed(0); // Display numbers without decimals
            }
          }
        },
        fill: {
          opacity: 1
        },
        legend: {
          position: 'bottom',
          horizontalAlign: 'left',
          offsetX: 40
        }
      };

      var chart = new ApexCharts(document.querySelector("#enps3"), options);
      chart.render();


});