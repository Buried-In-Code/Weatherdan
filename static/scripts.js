const unique = (arr) => [...new Set(arr)];

const headers = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function loadYearlyStats(maximum = 1000){
  fetch(`/api/v0/yearly-stats?maximum=${maximum}`, {
    method: "GET",
    headers,
  })
  .then((response) => {
    if (response.ok){
      return response.json();
    }
    return Promise.reject(response);
  })
  .then((data) => {
    let labelList = [];
    let entryData = [];
    data.forEach((stat) => {
      labelList.push(stat.timestamp);
      entryData.push(stat.value);
    });
    let entryList = [{
      label: "Label",
      fill: true,
      backgroundColor: "rgba(65,105,225,0.1)",
      borderColor: "rgba(65,105,225,1)",
      data: entryData,
      steppedLine: false
    }];
    createGraph("yearly-stats", labelList, entryList);
  })
  .catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText}: ${msg.details}`);
  }));
}

function loadMonthlyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0
  fetch(`/api/v0/monthly-stats?year=${year}&maximum=${maximum}`, {
    method: "GET",
    headers,
  })
  .then((response) => {
    if (response.ok){
      return response.json();
    }
    return Promise.reject(response);
  })
  .then((data) => {
    let labelList = [];
    let entryData = [];
    data.forEach((stat) => {
      labelList.push(stat.timestamp);
      entryData.push(stat.value);
    });
    let entryList = [{
      label: "Label",
      fill: true,
      backgroundColor: "rgba(65,105,225,0.1)",
      borderColor: "rgba(65,105,225,1)",
      data: entryData,
      steppedLine: false
    }];
    createGraph("monthly-stats", labelList, entryList);
  })
  .catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText}: ${msg.details}`);
  }));
}

function loadWeeklyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0;
  let month = params.get("month");
  if (month == "" || month == null)
    month = 0;
  fetch(`/api/v0/weekly-stats?year=${year}&month=${month}&maximum=${maximum}`, {
    method: "GET",
    headers,
  })
  .then((response) => {
    if (response.ok){
      return response.json();
    }
    return Promise.reject(response);
  })
  .then((data) => {
    let labelList = [];
    let entryData = [];
    data.forEach((stat) => {
      labelList.push(stat.timestamp);
      entryData.push(stat.value);
    });
    let entryList = [{
      label: "Label",
      fill: true,
      backgroundColor: "rgba(65,105,225,0.1)",
      borderColor: "rgba(65,105,225,1)",
      data: entryData,
      steppedLine: false
    }];
    createGraph("weekly-stats", labelList, entryList);
  })
  .catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText}: ${msg.details}`);
  }));
}

function loadDailyStats(maximum = 1000){
  let params = new URLSearchParams(window.location.search);
  let year = params.get("year");
  if (year == "" || year == null)
    year = 0;
  let month = params.get("month");
  if (month == "" || month == null)
    month = 0;
  fetch(`/api/v0/daily-stats?year=${year}&month=${month}&maximum=${maximum}`, {
    method: "GET",
    headers,
  })
  .then((response) => {
    if (response.ok){
      return response.json();
    }
    return Promise.reject(response);
  })
  .then((data) => {
    let labelList = [];
    let entryData = [];
    data.forEach((stat) => {
      labelList.push(stat.timestamp);
      entryData.push(stat.value);
    });
    let entryList = [{
      label: "Label",
      fill: true,
      backgroundColor: "rgba(65,105,225,0.1)",
      borderColor: "rgba(65,105,225,1)",
      data: entryData,
      steppedLine: false
    }];
    createGraph("daily-stats", labelList, entryList);
  })
  .catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText}: ${msg.details}`);
  }));
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
