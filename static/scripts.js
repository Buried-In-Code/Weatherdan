function loadYearlyStats(maximum = 1000){
  $.ajax({
    async: false,
    url: "/api/v0/yearly-stats?maximum=" + maximum,
    type: "GET",
    dataType: "json",
    success: function (data) {
      createGraph("yearly-stats", Object.keys(data), [{
        label: "Yearly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data),
        steppedLine: false
      }]);
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
      createGraph("monthly-stats", Object.keys(data), [{
        label: "Monthly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data),
        steppedLine: false
      }]);
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
      createGraph("weekly-stats", Object.keys(data), [{
        label: "Weekly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data),
        steppedLine: false
      }]);
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
      createGraph("daily-stats", Object.keys(data), [{
        label: "Daily",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data),
        steppedLine: false
      }]);
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
          display: false
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
    window.location = "/Weatherdan/filtered";
  else
    window.location = "/Weatherdan/filtered?year=" + year;
}

function setMonth(month){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (month == 0)
    window.location = "/Weatherdan/filtered?year=" + year;
  else
    window.location = "/Weatherdan/filtered?year=" + year + "&month=" + month;
}
