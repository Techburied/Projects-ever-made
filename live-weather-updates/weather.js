function weather(){
  fetch('https://api.openweathermap.org/data/2.5/weather?q=jaipur&appid=06c921750b9a82d8f5d1294e1586276f')
  .then(response => response.json())
  .then(data => {
    let temp = Math.round(data['main']['temp']-273);
    let cond = data['weather'][0]['main'];
    let wind = Math.round(data['wind']['speed']*1.609344)
    let pressure = Math.round(data['main']['pressure']* 0.029530)
    let humid = data['main']['humidity']-6;
    
    document.getElementById('temp').innerHTML= temp+"°";
    document.getElementById('cond').innerText = cond;
    document.getElementById('wind').innerText = wind+" Km/h";
    document.getElementById('press').innerText = pressure+" in";
    document.getElementById('humid').innerText = humid+" %";
  }); 
  
fetch('https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400')
  .then(response => response.json())
  .then(data => {
    let rise = data.results.sunrise;
    document.getElementById('rise').innerText = rise;
  });

}

setInterval(weather,1000)