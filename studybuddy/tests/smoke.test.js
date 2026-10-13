const {JSDOM}=require('jsdom'),fs=require('fs');
const html=fs.readFileSync('../index.html','utf8').replace(/<link[^>]*>/,'');
const errs=[];const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://x.test/',pretendToBeVisual:true,beforeParse(w){w.confirm=()=>true;w.matchMedia=()=>({matches:false,addEventListener(){},removeEventListener(){}});w.ResizeObserver=class{observe(){}disconnect(){}};w.IntersectionObserver=class{observe(){}disconnect(){}};w.scrollTo=()=>{};w.Element.prototype.scrollTo=()=>{};w.addEventListener('error',e=>errs.push(e.message))}});
const w=dom.window,E=s=>w.eval(s),log=(k,v)=>console.log(k,v);
const wait=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
log('landing',w.document.body.textContent.includes('Learn Happy'));
E("S.ob.d={name:'Hashim',course:'cseai',sem:4,subjects:['Python','ML','DSA','DBMS'],dur:10,diff:'Adaptive',mode:'mixed',goal:10};S.ob.step=5;onext()");
await wait(50);log('user',E('S.user&&S.user.name'));
for(const r of ['home','subjects','discover','history','progress','ach','prof','mistakes']){E(`location.hash='${r}'`);await wait(30);log(r,w.document.querySelector('#pg').innerHTML.length>200)}
E("startG('DBMS-quiz')");await wait(30);log('playing',!!w.document.querySelector('.opt'));
for(let i=0;i<5;i++){E(i==1?"pick(0)":"pick(QM[S.cur.items[S.cur.i]].a)");E('nextQ()');await wait(10)}
await wait(30);const ss=E('S.sessions[0]');log('result',JSON.stringify({acc:ss.acc,xp:ss.xp,ach:ss.newAch,hash:w.location.hash.slice(0,8)}));
E("startG('DBMS-quiz')");for(let i=0;i<5;i++){E(`pick(QM[S.cur.items[S.cur.i]].a)`);E('nextQ()')}
log('xp after improve',E('S.xp'));
E("startG('DBMS-quiz')");for(let i=0;i<5;i++){E(`pick(QM[S.cur.items[S.cur.i]].a)`);E('nextQ()')}
log('xp after replay (no farm)',E('S.xp'));
E("startG('ML-flash')");for(let i=0;i<4;i++){E('rate(2)')}log('flash due',JSON.stringify(E('Object.keys(S.cards).length')));
E("startG('Python-chal')");E('pick(-1)');E('finish(true)');log('abandon',E('S.sessions.slice(-1)[0].status'));
E("location.hash='mistakes'");await wait(30);log('mistakes ok',w.document.querySelector('#pg').textContent.includes('Review Mistakes'));
E("retry(['DBMS-q2'])");E('pick(QM["DBMS-q2"].a)');E('nextQ()');log('streak',JSON.stringify(E('streaks()')));
E("location.hash='progress'");await wait(30);log('progress',w.document.querySelector('#pg').textContent.includes('Study minutes'));
E("startG('OS-quiz')");E('pick(0)');w.eval("S.cur.i=0");dom.reconfigure&&0;
log('persisted',!!E("JSON.parse(localStorage.getItem('studybuddy.v1')).cur"));

E("S.out=true;save();location.hash='login'");await wait(60);log('login page',!!w.document.querySelector('.gp canvas')&&w.document.body.textContent.includes('Welcome back'));
E("S.out=false;save();location.hash='home'");await wait(30);
E("S=def();save();location.hash='login'");await wait(60);log('new login form',!!w.document.querySelector('#ln'));
w.document.querySelector('#ln').value='';E("lsub({preventDefault(){}})");log('empty name blocked',w.document.querySelector('#le').textContent);
w.document.querySelector('#ln').value='Asha';E("lsub({preventDefault(){}})");await wait(40);log('to onboarding',w.location.hash+' '+E('S.ob.d.name'));
log('errors',errs.join('|')||'none');
})();
