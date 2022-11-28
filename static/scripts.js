const unique = (arr) => [...new Set(arr)];

function loadYearlyStats(maximum = 1000){
  $.ajax({
    async: false,
    url: "/api/v0/yearly-stats?maximum=" + maximum,
    type: "GET",
    dataType: "json",
    success: function (data) {
      let graphLabels = [];
      data.forEach(function(device){
        device.stats.forEach(function(stat){
          graphLabels.push(stat.timestamp);
        });
      });
      graphLabels = unique(graphLabels);
      let graphData = [];
      data.forEach(function(device){
        let entryData = [];
        device.stats.forEach(function(stat){
          entryData.push(stat.value);
        });

        let entry = {
          label: device.name,
          fill: true,
          backgroundColor: "rgba(65,105,225,0.1)",
          borderColor: "rgba(65,105,225,1)",
          data: entryData,
          steppedLine: false
        };
        graphData.push(entry);
      });
      createGraph("yearly-stats", graphLabels, graphData);
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function loadMonthlyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0
  $.ajax({
    async: false,
    url: "/api/v0/monthly-stats?year=" + year + "&maximum=" + maximum,
    type: "GET",
    dataType: "json",
    success: function(data){
      let graphLabels = [];
      data.forEach(function(device){
        device.stats.forEach(function(stat){
          graphLabels.push(stat.timestamp);
        });
      });
      graphLabels = unique(graphLabels);
      let graphData = [];
      data.forEach(function(device){
        let entryData = [];
        device.stats.forEach(function(stat){
          entryData.push(stat.value);
        });

        let entry = {
          label: device.name,
          fill: true,
          backgroundColor: "rgba(65,105,225,0.1)",
          borderColor: "rgba(65,105,225,1)",
          data: entryData,
          steppedLine: false
        };
        graphData.push(entry);
      });
      createGraph("monthly-stats", graphLabels, graphData);
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function loadWeeklyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0;
  let month = params.get("month");
  if (month == "" || month == null)
    month = 0;
  $.ajax({
    async: false,
    url: "/api/v0/weekly-stats?year=" + year + "&month=" + month + "&maximum=" + maximum,
    type: "GET",
    dataType: "json",
    success: function(data){
      let graphLabels = [];
      data.forEach(function(device){
        device.stats.forEach(function(stat){
          graphLabels.push(stat.timestamp);
        });
      });
      graphLabels = unique(graphLabels);
      let graphData = [];
      data.forEach(function(device){
        let entryData = [];
        device.stats.forEach(function(stat){
          entryData.push(stat.value);
        });

        let entry = {
          label: device.name,
          fill: true,
          backgroundColor: "rgba(65,105,225,0.1)",
          borderColor: "rgba(65,105,225,1)",
          data: entryData,
          steppedLine: false
        };
        graphData.push(entry);
      });
      createGraph("weekly-stats", graphLabels, graphData);
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function loadDailyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0;
  let month = params.get("month");
  if (month == "" || month == null)
    month = 0;
  $.ajax({
    async: false,
    url: "/api/v0/daily-stats?year=" + year + "&month=" + month + "&maximum=" + maximum,
    type: "GET",
    dataType: "json",
    success: function(data){
      let graphLabels = [];
      data.forEach(function(device){
        device.stats.forEach(function(stat){
          graphLabels.push(stat.timestamp);
        });
      });
      graphLabels = unique(graphLabels);
      let graphData = [];
      data.forEach(function(device){
        let entryData = [];
        device.stats.forEach(function(stat){
          entryData.push(stat.value);
        });

        let entry = {
          label: device.name,
          fill: true,
          backgroundColor: "rgba(65,105,225,0.1)",
          borderColor: "rgba(65,105,225,1)",
          data: entryData,
          steppedLine: false
        };
        graphData.push(entry);
      });
      createGraph("daily-stats", graphLabels, graphData);
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function createGraph(name, labels, dataset, type = 'line') {
  let ctx = document.getElementById(name);
  new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: dataset
    },
    options: {
      plugins: {
        legend: {
          labels: {
            fontColor: '#D0D0D0',
            fontSize: 14
          },
          display: true
        }
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            maxRotation: 90,
            minRotation: 90
          },
          title: {
            display: true,
            text: 'Timestamp'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Rainfall (mm)'
          }
        }
      }
    }
  });
}

function setYear(year, caller){
  if (year == 0)
    window.location = "/weatherdan/filtered";
  else
    window.location = "/weatherdan/filtered?year=" + year;
}

function setMonth(month){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (month == 0)
    window.location = "/weatherdan/filtered?year=" + year;
  else
    window.location = "/weatherdan/filtered?year=" + year + "&month=" + month;
}
