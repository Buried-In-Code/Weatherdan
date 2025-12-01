function ready(callback) {
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", callback);
  else
    callback();
}

function getBulmaColour(name) {
  const tempElement = document.createElement("div");
  tempElement.className = `has-background-${name}`;
  document.body.appendChild(tempElement);
  const computedStyle = getComputedStyle(tempElement);
  const colour = computedStyle.backgroundColor;
  document.body.removeChild(tempElement);
  return colour;
}

function createChart(ctx, unit) {
  new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        data: []
      }]
    },
    options: {
      interaction: {
        intersect: false,
        mode: "nearest"
      },
      plugins: {
        legend: {
          display: false,
          labels: {
            color: getBulmaColour("text")
          }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.formattedValue} ${unit}`
          }
        }
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Timestamp",
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
            text: unit,
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
  });
}
