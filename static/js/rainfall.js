function loadRainfallStats(timeframe, graphId, count = null) {
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
      data.forEach(function (reading, index) {
        if (count != null && index >= count)
          return;
        if (timeframe == "Daily")
          labelList.push(moment(reading.datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Weekly")
          labelList.push(moment(reading.start_datestamp).format("Do MMM YYYY"));
        else if (timeframe == "Monthly")
          labelList.push(moment(reading.datestamp).format("MMM YYYY"));
        else if (timeframe == "Yearly")
          labelList.push(moment(reading.datestamp).format("YYYY"));
        entryData.push(reading.total);
      });
      createGraph(graphId, labelList, entryData, "Rainfall", "mm", "line");
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
