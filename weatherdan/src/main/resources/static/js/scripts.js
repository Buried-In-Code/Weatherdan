function ready(callback) {
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", callback);
  else
    callback();
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
          display: false
        }
      },
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Timestamp"
          },
          position: "bottom"
        },
        y: {
          title: {
            display: true,
            text: unit
          },
          position: "left",
          beginAtZero: false
        }
      }
    }
  });
}
