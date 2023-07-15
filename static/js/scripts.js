const unique = (arr) => [...new Set(arr)];
const headers = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function ready(fn) {
  if (document.readyState !== "loading") {
    fn();
    return;
  }
  document.addEventListener("DOMContentLoaded", fn);
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function addLoading(caller){
  let element = document.getElementById(caller);
  element.classList.add("is-loading");
}

function removeLoading(caller){
  let element = document.getElementById(caller);
  element.classList.remove("is-loading");
}

function setTheme(){
  let darkCss = document.getElementById("dark-theme");
  let lightCss = document.getElementById("light-theme");
  let theme = getCookie("theme");
  if (theme == "light"){
    darkCss.disabled = true;
    lightCss.disabled = false;
  } else {
    darkCss.disabled = false;
    lightCss.disabled = true;
  }
}

function changeTheme(){
  let currentTheme = getCookie("theme");
  let newTheme = "dark";
  if (currentTheme == "dark")
    newTheme = "light";

  document.cookie = `theme=${newTheme};path=/;max-age=${60*60*24*30};SameSite=Strict`;
  setTheme();
}

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

function loadDailyStats(count = 1000) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/stats/daily?" + new URLSearchParams({
    year: params.get("year") || 0,
    month: params.get("month") || 0,
    count: count
  }), {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labelList = [];
      let entryData = [];
      data.forEach((reading) => {
        labelList.push(moment(reading.timestamp).format("Do MMM YYYY"));
        entryData.push(reading.value);
      });
      createGraph("daily-stats", labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

function loadWeeklyStats(count = 1000) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/stats/weekly?" + new URLSearchParams({
    year: params.get("year") || 0,
    month: params.get("month") || 0,
    count: count
  }), {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labelList = [];
      let entryData = [];
      data.forEach((reading) => {
        labelList.push(moment(reading.start_timestamp).format("Do MMM YYYY"));
        entryData.push(reading.value);
      });
      createGraph("weekly-stats", labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

function loadMonthlyStats(count = 1000) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/stats/monthly?" + new URLSearchParams({
    year: params.get("year") || 0,
    count: count
  }), {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labelList = [];
      let entryData = [];
      data.forEach((reading) => {
        labelList.push(moment(reading.timestamp).format("MMM YYYY"));
        entryData.push(reading.value);
      });
      createGraph("monthly-stats", labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

function loadYearlyStats(count = 1000) {
  fetch("/api/stats/yearly?" + new URLSearchParams({
    count: count
  }), {
    method: "GET",
    headers: headers
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labelList = [];
      let entryData = [];
      data.forEach((reading) => {
        labelList.push(moment(reading.timestamp).format("YYYY"));
        entryData.push(reading.value);
      });
      createGraph("yearly-stats", labelList, entryData);
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`)
  }));
}

ready(setTheme);
