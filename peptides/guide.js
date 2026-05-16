document.addEventListener('DOMContentLoaded',function(){
  var btn=document.getElementById('hamburger');
  var nav=document.querySelector('.nav-links');
  var navEl=document.querySelector('nav');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      btn.classList.toggle('open');
      nav.classList.toggle('open');
      if(navEl)navEl.classList.toggle('nav-open');
    });
  }
  document.querySelectorAll('details.faq-item').forEach(function(d){
    var s=d.querySelector('summary');
    if(s){s.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();d.open=!d.open;});}
  });
  var crumb=document.querySelector('.crumb');
  if(crumb){
    var parts=crumb.textContent.split('/');
    var peptideName=parts[parts.length-1].trim();
    if(peptideName&&peptideName!=='Peptides'){
      var bc={
        "@context":"https://schema.org",
        "@type":"BreadcrumbList",
        "itemListElement":[
          {"@type":"ListItem","position":1,"name":"Home","item":"https://thepeptideradar.com/"},
          {"@type":"ListItem","position":2,"name":"Peptide Guides","item":"https://thepeptideradar.com/peptides/"},
          {"@type":"ListItem","position":3,"name":peptideName,"item":"https://thepeptideradar.com"+window.location.pathname}
        ]
      };
      var s=document.createElement('script');
      s.type='application/ld+json';
      s.textContent=JSON.stringify(bc);
      document.head.appendChild(s);
    }
  }
});
