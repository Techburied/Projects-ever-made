let day = document.getElementById('days')
let hour = document.getElementById('hours')
let mins = document.getElementById('mins')
let secs = document.getElementById('seconds')
let host = document.getElementById('host-bt')
let links = document.getElementsByClassName('host-links')

var countDownDate = new Date("Jan 1, 2023 24:00:00").getTime();


var x = setInterval(function() {

  var now = new Date().getTime();

  // Find the 
  var distance = countDownDate - now;

  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  day.innerHTML = days + ' D'
  hour.innerHTML = hours + ' H'
  mins.innerHTML = minutes + ' M'
  secs.innerHTML = seconds + ' S'
 

  if (distance < 0) {
    clearInterval(x);
    document.getElementById("countdown").innerHTML = "EXPIRED";
  }
}, 1000);

host.addEventListener('click',function f1() {
  host.classList.add('v')
});
