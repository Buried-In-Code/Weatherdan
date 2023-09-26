function createGraph(elementId, labelList, entryData) {
  var config = {
    type: "bar",
    data: {
      labels: labelList,
      datasets: [
        {
          label: "Humidity",
          backgroundColor: "rgba(76,76,255,0.2)",
          borderColor: "rgba(76,76,255,1)",
          borderWidth: 2,
          borderSkipped: false,
          data: entryData,
          yAxisID: "y",
        }
      ]
    },
    options: {
      interaction: {
        intersect: false,
        mode: "nearest",
      },
      plugins: {
        legend: {
          display: false
        },
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Timestamp",
          },
          position: "bottom",
        },
        y: {
          title: {
            display: true,
            text: "Humidity (%)"
          },
          position: "left",
        }
      }
    }
  }
  let ctx = document.getElementById(elementId);
  new Chart(ctx, config);
}

function loadStats(timeframe, graphId) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/humidity?" + new URLSearchParams({
    timeframe: timeframe,
    year: params.get("year") || 0,
    month: params.get("month") || 0,
  }), {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labelList = [];
      let entryData = [];
      data.forEach((reading) => {
        if (timeframe == "Daily")
          labelList.push(moment(reading.datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Weekly")
          labelList.push(moment(reading.start_datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Monthly")
          labelList.push(moment(reading.datestamp).format("MMM YYYY"));
        else if (timeframe == "Yearly")
          labelList.push(moment(reading.datestamp).format("YYYY"));
        entryData.push([reading.high, reading.low]);
      });
      createGraph(graphId, labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
