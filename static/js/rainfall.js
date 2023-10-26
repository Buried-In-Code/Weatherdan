function loadRainfallStats(timeframe, graphId, count = null) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/rainfall?" + new URLSearchParams({
    timeframe: timeframe,
    year: params.get("year") || 0,
    month: params.get("month") || 0,
    allResults: count != null,
  }), {
    method: "GET",
    headers: headers,
  }).then((response) => {
    if (!response.ok)
      return Promise.reject(response);
    response.json().then((data) => {
      let labels = [];
      let datasets = [];
      let entryData = [];
      let entryCount = data.length - count;
      data.forEach(function (x, index) {
        if (count != null && index < entryCount)
          return;
        if (timeframe == "Daily")
          labels.push(moment(x.datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Weekly")
          labels.push(moment(x.start_datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Monthly")
          labels.push(moment(x.datestamp).format("MMM YYYY"));
        else if (timeframe == "Yearly")
          labels.push(moment(x.datestamp).format("YYYY"));
        entryData.push(x.value);
      });
      datasets.push({
        data: entryData,
        label: "Total",
        type: "line",
        backgroundColor: backgroundColours[0],
        borderColor: borderColours[0],
        borderWidth: 2,
        borderSkipped: false,
      });
      createGraph(graphId, labels, datasets, "mm", "Millimeters");
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
