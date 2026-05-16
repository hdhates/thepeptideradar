document.addEventListener('DOMContentLoaded',function(){
  var btn=document.getElementById('hamburger');
  var nav=document.querySelector('.nav-links');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      btn.classList.toggle('open');
      nav.classList.toggle('open');
    });
  }
  document.querySelectorAll('details.faq-item').forEach(function(d){
    var s=d.querySelector('summary');
    if(s){s.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();d.open=!d.open;});}
  });
});
