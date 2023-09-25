function createGraph(elementId, labelList, entryData) {
  let ctx = document.getElementById(elementId);
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labelList,
      datasets: [{
        backgroundColor: "rgba(65,105,225,0.1)",
        borderColor: "rgba(65,105,225,1)",
        data: entryData,
        steppedLine: false,
        fill: true,
      }]
    },
    options: {
      interaction: {
        intersect: false,
        mode: "nearest",
      },
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: true,
          callbacks: {
            label: function (context) {
              return context.formattedValue + "mm";
            }
          }
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
            text: "Rainfall (mm)",
          },
          position: "left",
        }
      },
    }
  });
}

function loadStats(timeframe, graphId) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/rainfall?" + new URLSearchParams({
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
        entryData.push(reading.value);
      });
      createGraph(graphId, labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
