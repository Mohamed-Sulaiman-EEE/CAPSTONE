

function refresh_gps(trip_id)
{
  if (navigator.geolocation) 
  {
  res = navigator.geolocation.getCurrentPosition();

  }
  lat = res.latitude
  lat = 0
  lon = res.latitude
  fetch("/conductor-utility-refresh-gps" , {
    method : "POST" , 
    body : JSON.stringify({trip_id : trip_id , gps : lat}),
  
  });
  
};






function getLocation(gps) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition();
  } 
  fetch("/test-gps", 
  {
    method: "POST",
    body: JSON.stringify({ data : gps }),
  });

}

function showPosition(position) {
  let d = "Latitude: " + position.coords.latitude +
  "Longitude: " + position.coords.longitude;
  console.log(d);
  fetch("/test-gps", 
  {
    method: "POST",
    body: JSON.stringify({ data : gps }),
  }
  ).then((_res) => {
    window.location.href = "/conductor-home";
  });;

}







function test_js(trip_id) 
{
  console.log(trip_id);
  fetch("/test-js", 
  {
    method: "POST",
    body: JSON.stringify({ trip_id : trip_id  }),
  }
  ).then((_res) => {
    window.location.href = "/conductor-home";
  });;
}