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

function addLoading(caller) {
  const element = document.getElementById(caller);
  element.classList.add("is-loading");
}

function removeLoading(caller) {
  const element = document.getElementById(caller);
  element.classList.remove("is-loading");
}

function resetForm(page) {
  window.location = page;
}

function setTheme() {
  const darkCss = document.getElementById("dark-theme");
  const lightCss = document.getElementById("light-theme");
  const theme = getCookie("weatherdan_theme");

  if (darkCss !== null && lightCss !== null) {
    darkCss.disabled = theme == "dark";
    lightCss.disabled = theme == "light";
  }
}

function toggleTheme() {
  const currentTheme = getCookie("weatherdan_theme");
  const newTheme = currentTheme === "dark" ? "light" : "dark";

  document.cookie = `weatherdan_theme=${newTheme}; path=/; max-age=${60 * 60 * 24 * 30}; SameSite=Strict`;
  setTheme();
}

ready(setTheme);

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
    return response.status !== 204 ? response.json() : "";
  } catch(error) {
    alert(`${error.status} ${error.statusText}: ${await error.text()}`);
    return null;
  }
}

const backgroundColours = [
  "rgba(65,105,225,0.1)",
  "rgba(255,65,105,0.1)",
  "rgba(105,255,65,0.1)",
];

const borderColours = [
  "rgba(65,105,225,1)",
  "rgba(255,65,105,1)",
  "rgba(105,255,65,1)",
];

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
          display: datasets.length > 1
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
          },
          position: "bottom",
        },
        y: {
          title: {
            display: true,
            text: unitLabel
          },
          position: "left",
          beginAtZero: false,
        }
      }
    }
  }
  console.log(config);
  new Chart(document.getElementById(elementId), config);
}

async function refreshData(endpoint) {
  let caller = "loading";

  addLoading(caller);
  try {
    const response = await fetch(endpoint, {
        method: "PUT",
        headers: HEADERS
    });

    if (!response.ok)
      throw response;
    if (response.status != 208)
      window.location.reload();
  } catch(error) {
    alert(`${error.status} ${error.statusText}: ${await error.text()}`);
  }
  removeLoading(caller);
}
