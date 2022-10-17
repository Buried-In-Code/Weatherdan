function addUser(){
  const username = document.getElementById("usernameEntry").value;
  $.ajax({
    async: false,
    url: "/api/v0/users",
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({
      "username": username
    }),
    success: function(){
      window.location = "/Weatherdan/" + username;
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function selectUser(){
  const username = document.getElementById("usernameEntry").value;
  $.ajax({
    async: false,
    url: "/api/v0/" + username,
    type: "GET",
    dataType: "json",
    success: function(){
      window.location = "/Weatherdan/" + username;
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}

function loadInfo(username) {
  $.ajax({
    async: false,
    url: "/api/v0/" + username + "/stats",
    type: 'GET',
    dataType: 'json',
    success: function (data) {
      createGraph("daily-stats", Object.keys(data.daily), [{
        label: "Daily",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data.daily),
        steppedLine: false
      }])
      createGraph("weekly-stats", Object.keys(data.weekly), [{
        label: "Weekly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data.weekly),
        steppedLine: false
      }])
      createGraph("monthly-stats", Object.keys(data.monthly), [{
        label: "Monthly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data.monthly),
        steppedLine: false
      }])
      createGraph("yearly-stats", Object.keys(data.yearly), [{
        label: "Yearly",
        fill: true,
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: Object.values(data.yearly),
        steppedLine: false
      }])
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

function addRainfall(username){
  const dateStr = document.getElementById("dateEntry").value;
  let dayField = dateStr.split("-")[0];
  let monthField = dateStr.split("-")[1];
  let yearField = dateStr.split("-")[2];
//  let timestamp = new Date(yearField, monthField, dayField);
  const valueStr = document.getElementById("rainfallEntry").value;
  $.ajax({
    async: false,
    url: "/api/v0/" + username + "/stats",
    type: "POST",
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({
      "timestamp": yearField + "-" + monthField + "-" + dayField,
      "value": valueStr
    }),
    success: function(){
      window.location.reload();
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + "\nStatus Text: " + xhr.statusText + "\n" + xhr.responseText);
    }
  });
}
