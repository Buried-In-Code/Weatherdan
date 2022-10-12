function addUser(){
  const username = document.getElementById("usernameEntry").value;
  $.ajax({
    async: false,
    url: "/api/v0/users",
    type: "POST",
    headers: {
      accept: "application/json",
      contentType: "application/json"
    },
    dataType: "json",
    data: JSON.stringify({
      "username": username
    }),
    success: function(){
      window.location = "/Weatherdan/" + username;
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + " Status Text: " + xhr.statusText + " " + xhr.responseText);
    }
  });
}

function selectUser(){
  const username = document.getElementById("usernameEntry").value;
  $.ajax({
    async: false,
    url: "/api/v0/" + username,
    type: "GET",
    headers: {
      accept: "application/json",
      contentType: "application/json"
    },
    dataType: "json",
    success: function(){
      window.location = "/Weatherdan/" + username;
    },
    error: function(xhr){
      alert("Request Status: " + xhr.status + " Status Text: " + xhr.statusText + " " + xhr.responseText);
    }
  });
}

function loadInfo(username) {
	$.ajax({
		async: false,
		url: "/api/v0/" + username + "/stats",
		type: 'GET',
		headers: {
			accept: 'application/json',
			contentType: 'application/json'
		},
		dataType: 'json',
		success: function (data) {
		  createGraph("daily-stats", Object.keys(data.daily), [{
		    label: "Daily",
		    fill: true,
		    backgroundColor: "rgba(0,0,192,0.5)",
		    borderColor: "rgba(0,0,192,1)",
		    data: Object.values(data.daily),
		    steppedLine: false
		  }])
		  createGraph("weekly-stats", Object.keys(data.weekly), [{
		    label: "Weekly",
		    fill: true,
		    backgroundColor: "rgba(0,0,192,0.5)",
		    borderColor: "rgba(0,0,192,1)",
		    data: Object.values(data.weekly),
		    steppedLine: false
		  }])
		  createGraph("monthly-stats", Object.keys(data.monthly), [{
		    label: "Monthly",
		    fill: true,
		    backgroundColor: "rgba(0,0,192,0.5)",
		    borderColor: "rgba(0,0,192,1)",
		    data: Object.values(data.monthly),
		    steppedLine: false
		  }])
		  createGraph("yearly-stats", Object.keys(data.yearly), [{
		    label: "Yearly",
		    fill: true,
		    backgroundColor: "rgba(0,0,192,0.5)",
		    borderColor: "rgba(0,0,192,1)",
		    data: Object.values(data.yearly),
		    steppedLine: false
		  }])
		},
    error: function(xhr){
      alert("Request Status: " + xhr.status + " Status Text: " + xhr.statusText + " " + xhr.responseText);
    }
	});
}

function createGraph(name, labels, dataset, type = 'bar') {
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
