function test_js(trip_id , a) 
{
  console.log(trip_id);
  test = 55;
  fetch("/test-js", 
  {
    method: "POST",
    body: JSON.stringify({ trip_id : trip_id , a : a , test : test  }),
  }
  ).then((_res) => {
    window.location.href = "/conductor-home";
  });;
}


//-------- REFRESH GPS-----------
function refreshGPS() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  let gps = position.coords.latitude +"," + position.coords.longitude;
  fetch("/conductor-utility-refresh-gps", 
  {
    method: "POST",
    body: JSON.stringify({ gps : gps }),
  }
  ).then((_res) => {
    window.location.href = "/conductor-current-trip";
  });;
}

//-------- REFRESH GPS-----------