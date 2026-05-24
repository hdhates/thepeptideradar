document.addEventListener('DOMContentLoaded',function(){
  var btn=document.getElementById('hamburger');
  var nav=document.querySelector('.nav-links');
  var navEl=document.querySelector('nav');
  var overlay=document.getElementById('nav-overlay');
  if(btn&&nav){
    btn.addEventListener('click',function(){
      btn.classList.toggle('open');
      nav.classList.toggle('open');
      if(navEl)navEl.classList.toggle('nav-open');
      if(overlay)overlay.classList.toggle('open');
    });
  }
  if(overlay){
    overlay.addEventListener('click',function(){
      btn.classList.remove('open');
      nav.classList.remove('open');
      if(navEl)navEl.classList.remove('nav-open');
      overlay.classList.remove('open');
    });
  }
  document.querySelectorAll('details.faq-item').forEach(function(d){
    var s=d.querySelector('summary');
    if(s){s.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();d.open=!d.open;});}
  });
  document.querySelectorAll('.card-cta').forEach(function(link){
    link.addEventListener('click',function(){
      var card=this.closest('.card');
      var nameEl=card&&card.querySelector('.card-name');
      var name=nameEl?nameEl.textContent.trim():'';
      if(typeof gtag==='function'){
        gtag('event','Clicked Supplier - Visit Site',{supplier_name:name,supplier_url:this.href,page_peptide:document.title.split('—')[0].replace('Where to Buy','').trim()});
      }
    });
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
