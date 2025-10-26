const payload = {
  start: "Start",
  end: "End",
  start_loc: { lat: 13.0827, lng: 80.2707 },
  end_loc: { lat: 13.05, lng: 80.25 }
};
const res = await fetch("http://127.0.0.1:8000/get_safe_route", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(payload)
});
const data = await res.json();
// data.route -> array of [lat,lng] pairs
// data.danger_zones -> array of zones
