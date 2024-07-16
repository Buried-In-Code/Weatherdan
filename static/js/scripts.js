const HEADERS = {
  "Accept": "application/json; charset=UTF-8",
  "Content-Type": "application/json; charset=UTF-8",
};

function ready(callback) {
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", callback);
  else
    callback();
}

function getCookie(cname) {
  const name = cname + "=";
  const cookies = decodeURIComponent(document.cookie).split(";");

  for (const cookie of cookies) {
    let _cookie = cookie.trim();
    if (_cookie.indexOf(name) == 0)
      return _cookie.substring(name.length);
  }
  return "";
}

function toggleLoading(caller) {
  const element = document.getElementById(caller);
  element.classList.toggle("is-loading");
}

function resetForm(page) {
  window.location = page;
}

function setTheme() {
  const theme = getCookie("weatherdan_theme");
  document.documentElement.setAttribute("data-theme", theme === "dark" ? "villain" : "hero");
}

function toggleTheme() {
  const currentTheme = getCookie("weatherdan_theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  document.cookie = `weatherdan_theme=${newTheme}; path=/; max-age=${60 * 60 * 24 * 30}; SameSite=Strict`;
  setTheme();
}

ready(() => {
    setTheme();
});

async function submitRequest(endpoint, method, body = {}) {
  try {
    const options = {
      method: method,
      headers: HEADERS,
    };
    if (method !== "GET")
      options.body = JSON.stringify(body);

    const response = await fetch(endpoint, options);

    if (!response.ok)
      throw response;
    const responseBody = response.status !== 204 ? await response.json() : "";
    return { status: response.status, body: responseBody }
  } catch(error) {
    alert(`${error.status} ${error.statusText}: ${await error.text()}`);
    return null;
  }
}

function getBulmaColour(name) {
  const tempElement = document.createElement("div");
  tempElement.className = `has-background-${name}`;
  document.body.appendChild(tempElement);
  const computedStyle = getComputedStyle(tempElement);
  const color = computedStyle.backgroundColor;
  document.body.removeChild(tempElement);
  return color;
}

function setAlpha(rgb, alpha) {
  const rgbValues = rgb.match(/\d+/g).map(Number);
  return `rgba(${rgbValues[0]}, ${rgbValues[1]}, ${rgbValues[2]}, ${alpha})`;
}

function getColours(alpha) {
  const colours = ["info", "danger", "success"];
  return colours.map(colour => setAlpha(getBulmaColour(colour), alpha));
}

function toggleChartLoading(id) {
  const progress = document.getElementById(`${id}-loading`).parentElement;
  const chart = document.getElementById(id).parentElement;
  progress.hidden = !progress.hidden;
  chart.hidden = !chart.hidden;
}

function createDataset(index, data, label, type, yAxisID = "y") {
  return {
    backgroundColor: getColours(0.5)[index],
    borderColor: getColours(1)[index],
    borderWidth: 2,
    borderSkipped: false,
    data: data,
    label: label,
    type: type,
    yAxisID: yAxisID
  }
}

function createGraph(elementId, labels, datasets, unit, unitLabel) {
  let config = {
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      interaction: {
        intersect: false,
        mode: "nearest",
      },
      plugins: {
        legend: {
          display: datasets.length > 1,
          labels: {
            color: getBulmaColour("text")
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              if (context.formattedValue.includes("[") && context.formattedValue.includes("]"))
                return JSON.parse(context.formattedValue).reverse().join(" - ") + unit;
              return context.formattedValue + unit
            }
          }
        }
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Date",
            color: getBulmaColour("text")
          },
          position: "bottom",
          ticks: {
            color: getBulmaColour("text")
          },
          grid: {
            color: getBulmaColour("text-50")
          }
        },
        y: {
          title: {
            display: true,
            text: unitLabel,
            color: getBulmaColour("text")
          },
          position: "left",
          beginAtZero: false,
          ticks: {
            color: getBulmaColour("text")
          },
          grid: {
            color: getBulmaColour("text-50")
          }
        }
      }
    }
  }
  new Chart(document.getElementById(elementId), config);
  toggleChartLoading(elementId);
}

async function refreshData(endpoint) {
  const response = await submitRequest(endpoint, "PUT");
  if (response !== null && response.status != 208)
      window.location.reload();
}

async function loadTotalStats(timeframe, graphId, endpoint, unit, unitLabel, maxEntries) {
  const currentParams = new URLSearchParams(window.location.search);
  const params = {
    timeframe: timeframe,
    year: currentParams.get("year") || 0,
    month: currentParams.get("month") || 0,
    "max-entries": maxEntries,
  };

  const response = await submitRequest(endpoint + "?" + new URLSearchParams(params), "GET");
  if (response !== null) {
    const labels = [];
    const datasets = [];
    let entryData = [];
    response.body.forEach((x, index) => {
      if (timeframe == "Yearly")
        labels.push(moment(x.datestamp).format("YYYY"));
      else if (timeframe == "Monthly")
        labels.push(moment(x.datestamp).format("MMM YYYY"));
      else if (timeframe == "Weekly")
        labels.push(moment(x.start_datestamp).format("Do MMM YYYY"));
      else
        labels.push(moment(x.datestamp).format("Do MMM YYYY"));
      entryData.push(x.value);
    });
    datasets.push(createDataset(0, entryData, "Total", "line"));
    createGraph(graphId, labels, datasets, unit, unitLabel);
  }
}

async function loadRainfallStats(timeframe, graphId, maxEntries = getCookie("weatherdan_max-entries") || 28) {
  await loadTotalStats(timeframe, graphId, "/api/rainfall", "mm", "Millimetres", maxEntries);
}

async function loadSolarStats(timeframe, graphId, maxEntries = getCookie("weatherdan_max-entries") || 28) {
  await loadTotalStats(timeframe, graphId, "/api/solar", "lx", "Lux", maxEntries);
}

async function loadUVIndexStats(timeframe, graphId, maxEntries = getCookie("weatherdan_max-entries") || 28) {
  await loadTotalStats(timeframe, graphId, "/api/uv-index", "", "Index", maxEntries);
}

async function loadWindStats(timeframe, graphId, maxEntries = getCookie("weatherdan_max-entries") || 28) {
  await loadTotalStats(timeframe, graphId, "/api/wind", "km/h", "Kilometers per Hour", maxEntries);
}
