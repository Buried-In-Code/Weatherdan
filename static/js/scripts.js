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
  for(let i = 0; i < ca.length; i++) {
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

function resetForm(page) {
  window.location = page;
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

function refreshData(endpoint) {
  let caller = "loading";

  addLoading(caller);
  fetch(endpoint, {
    method: "PUT",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    if (response.status != 208)
      window.location.reload();
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  })).finally(() => removeLoading(caller));
}
