var link = document.getElementById('searchBtn');
var input = document.getElementById("input");
var modal = document.getElementById("modal");
var countdown = document.getElementById("countdown");
var btn = document.getElementById("opener");
var span = document.getElementById("close");
var menu = document.getElementById("menu");
var profile = document.getElementById("profile");
var prbtn = document.getElementById("propener");
var main = document.getElementById('main');
var loader = document.getElementById('loader');
var linkEngine;

function imgRef() {
  main.style.backgroundImage = "url('https://source.unsplash.com/random/${4*screen.width}x${4*height}/?beautiful,nature,scene,natural')";
}
    
window.addEventListener("message", function(event) {
  linkEngine = event.data;
  updateLink();
});
    
function updateLink() {
  var search = encodeURIComponent(input.value);
  search = "https://685ee897-88fc-427c-9478-e84b75c634f6-00-2aa6o6h46iw9h.picard.replit.dev/search/" + search;
  link.setAttribute('href', search);
}

function loaded() {
  loader.style.display = "none";
  main.style.display = "block";
}

btn.onclick = function() { modal.style.display = "block"; menu.style.display = "block";}
prbtn.onclick = function() { modal.style.display = "block"; profile.style.display = "block";}
span.onclick = function() { modal.style.display = "none"; menu.style.display = "none"; profile.style.display = "none";}
