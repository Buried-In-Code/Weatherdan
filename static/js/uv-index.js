function loadStats(timeframe, graphId) {
  let params = new URLSearchParams(window.location.search);
  fetch("/api/uv-index?" + new URLSearchParams({
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
        entryData.push(reading.high);
      });
      createGraph(graphId, labelList, entryData, "UV Index", "", "line");
    });
  }).catch((response) => response.json().then((msg) => {
    alert(`${response.status} ${response.statusText} => ${msg.details}`);
  }));
}
