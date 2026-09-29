/* ===== SITE CONFIG: edit everything here ===== */
const SITE = {
  phone: "07494 831141",            // confirmed by owner 2026-09-29
  whatsapp: "447494831141",         // confirmed by owner 2026-09-29
  instagram: "https://www.instagram.com/unitybarbersnotts/",
  maps: "https://www.google.com/maps/search/?api=1&query=Unity+Barbers+166+Alfreton+Road+Nottingham+NG7+3NS",
  // confirmed by owner 2026-09-29: 9am to 11pm, 7 days
  hours: { Mon:[9,23], Tue:[9,23], Wed:[9,23], Thu:[9,23], Fri:[9,23], Sat:[9,23], Sun:[9,23] },
  // Confirmed by owner: cut & beard, shape up. Remaining prices still to confirm.
  menu: [
    { group:"Cuts", items:[
      ["Skin fade","Low, mid, high or drop. Blended to the skin.","£18"],
      ["Fade or taper","Clean blend with length left on top.","£16"],
      ["Scissor cut","Longer styles, texture and shape.","£16"],
      ["Buzz cut","One grade all over, lined up.","£10"],
      ["Kids' cut","Under 12s.","£12"]
    ]},
    { group:"Beard & grooming", items:[
      ["Shape up","Hairline shaped, lined and edged up.","£10"],
      ["Cut & beard","Any cut plus a full beard shape.","£20"],
      ["Hot towel treatment","Hot towel, lather and razor finish.","£10"],
      ["Eyebrow shape","Tidied with razor or trimmer.","£4"]
    ]},
    { group:"Designs & braids", items:[
      ["Hair design","Lines, parts and freestyle patterns.","from £5"],
      ["Cornrows","Straight-back or styled. Priced on length.","from £20"],
      ["Student cut","Any standard cut with valid student ID.","£14"]
    ]}
  ]
};
/* ============================================= */
(function(){
  const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
  if (new URLSearchParams(location.search).has('capture')) document.documentElement.classList.add('capture');
  const tel="tel:+44"+SITE.phone.replace(/\s/g,'').replace(/^0/,'');
  $$('[data-tel]').forEach(a=>a.href=tel);
  $$('[data-phone-label]').forEach(s=>s.textContent=(s.textContent==='Call'?'Call ':'')+SITE.phone);
  $$('[data-wa]').forEach(a=>a.href="https://wa.me/"+SITE.whatsapp);
  $$('[data-dir]').forEach(a=>a.href=SITE.maps);
  $$('[data-ig]').forEach(a=>a.href=SITE.instagram);
  $('#yr').textContent=new Date().getFullYear();

  const days=["Sun","Mon","Tue","Wed","Thu","Fri","Sat"], full={Mon:"Monday",Tue:"Tuesday",Wed:"Wednesday",Thu:"Thursday",Fri:"Friday",Sat:"Saturday",Sun:"Sunday"};
  const fmt=h=>{const x=h%24; return (x%12||12)+(x<12?"am":"pm");};
  const now=new Date(), today=days[now.getDay()], hrs=SITE.hours[today], hr=now.getHours()+now.getMinutes()/60;
  $('#hoursTable').innerHTML=Object.keys(full).map(d=>{const h=SITE.hours[d];return `<tr class="${d===today?'today':''}"><td>${full[d]}</td><td>${h?fmt(h[0])+' to '+fmt(h[1]):'Closed'}</td></tr>`}).join('');
  const allSame=Object.values(SITE.hours).every(h=>h&&h[0]===SITE.hours.Mon[0]&&h[1]===SITE.hours.Mon[1]);
  $('#footHours').innerHTML=allSame?`Every day<br>${fmt(SITE.hours.Mon[0])} to ${fmt(SITE.hours.Mon[1])}`:'See opening hours';
  const open=hrs&&hr>=hrs[0]&&hr<hrs[1];
  const sign=$('#sign');
  if(open){ $('#signState').textContent=`Open now until ${fmt(hrs[1])}`; }
  else { sign.classList.add('closed'); let n=null; for(let i=hrs&&hr<hrs[0]?0:1;i<8;i++){const d=days[(now.getDay()+i)%7]; if(SITE.hours[d]){n=[i,d];break;}}
    $('#signState').textContent=n?`Closed, opens ${n[0]===0?'today':n[0]===1?'tomorrow':full[n[1]]} at ${fmt(SITE.hours[n[1]][0])}`:'Closed'; }

  $('#menu').innerHTML=SITE.menu.map(g=>`<div class="menu-group"><h3>${g.group}</h3>${g.items.map(i=>`<div class="item"><span class="n">${i[0]}</span><span class="p">${i[2]}</span><p class="d">${i[1]}</p></div>`).join('')}</div>`).join('');

  const head=$('#head'), dock=$('#dock');
  const onScroll=()=>{ const y=scrollY; head.classList.toggle('solid',y>40); dock.classList.toggle('show',y>innerHeight*.55); };
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  const mm=$('#mmenu'), ob=$('#menuOpen');
  const setMenu=o=>{ mm.classList.toggle('open',o); mm.setAttribute('aria-hidden',!o); ob.setAttribute('aria-expanded',o); document.body.style.overflow=o?'hidden':''; if(o) $('#menuClose').focus(); };
  ob.onclick=()=>setMenu(true); $('#menuClose').onclick=()=>setMenu(false);
  $$('#mmenu nav a').forEach(a=>a.addEventListener('click',()=>setMenu(false)));

  const imgs=$$('#gallery img'), lb=$('#lb'), li=$('#lbImg'); let idx=0, last=null;
  const show=i=>{ idx=(i+imgs.length)%imgs.length; li.src=imgs[idx].src; li.alt=imgs[idx].alt; $('#lbCount').textContent=`${idx+1} / ${imgs.length}`; };
  const openLb=i=>{ last=document.activeElement; show(i); lb.classList.add('open'); document.body.style.overflow='hidden'; $('#lbClose').focus(); };
  const closeLb=()=>{ lb.classList.remove('open'); document.body.style.overflow=''; last&&last.focus(); };
  $$('#gallery button').forEach((b,i)=>b.onclick=()=>openLb(i));
  $('#lbClose').onclick=closeLb; $('#lbPrev').onclick=()=>show(idx-1); $('#lbNext').onclick=()=>show(idx+1);
  lb.addEventListener('click',e=>{ if(e.target===lb) closeLb(); });
  addEventListener('keydown',e=>{ if(lb.classList.contains('open')){ if(e.key==='Escape')closeLb(); if(e.key==='ArrowRight')show(idx+1); if(e.key==='ArrowLeft')show(idx-1);} else if(e.key==='Escape'&&mm.classList.contains('open')) setMenu(false); });
  let sx=null; lb.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});
  lb.addEventListener('touchend',e=>{ if(sx===null)return; const dx=e.changedTouches[0].clientX-sx; if(Math.abs(dx)>40) show(idx+(dx<0?1:-1)); sx=null; });
  window.__lb={openLb,show,closeLb,setMenu};
})();
