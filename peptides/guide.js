document.addEventListener('DOMContentLoaded',function(){
  var btn=document.getElementById('hamburger');
  var nav=document.querySelector('.nav-links');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      btn.classList.toggle('open');
      nav.classList.toggle('open');
    });
  }
});
