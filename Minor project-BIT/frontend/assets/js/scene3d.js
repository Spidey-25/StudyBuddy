/* StudyBuddy shared 3D scene: solid lit objects, scroll/route driven camera flight. Used by welcome.html and the app. */
(function(){
var $=function(s){return document.querySelector(s)},clamp=function(v,a,b){return Math.min(b,Math.max(a,v))},lerp=function(a,b,t){return a+(b-a)*t};
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches,root=document.documentElement;
var SUBJCODES=['C','CPP','JAVA','PYTHON','DSA','DBMS','OS','CN','WEB','SE','AI','ML','CYBER','CLOUD','EMBEDDED','IOT'];
var onTheme=function(){},api=window.SB3D={source:null,progress:0,retheme:function(){onTheme()}};
/* ---------- 3D scene: solid, lit objects (no wireframes) ---------- */
var cv=$('#gl'),ok=typeof THREE!=='undefined',R,mx=0,my=0;
if(ok){try{R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,powerPreference:'high-performance'})}catch(e){ok=false}}
var SP=0; /* smoothed scroll progress 0..1, shared with the CSS background */
if(ok){
 var lo=innerWidth<800,PR=Math.min(devicePixelRatio||1,lo?1.5:2),V3=THREE.Vector3,S=new THREE.Scene(),cam=new THREE.PerspectiveCamera(55,1,.1,500);
 R.setPixelRatio(PR);R.setClearColor(0x000000,0);R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.08;
 S.add(cam);S.fog=new THREE.Fog(0x05070f,52,240);
 function col(v){return new THREE.Color(getComputedStyle(root).getPropertyValue(v).trim())}
 /* lights ride with the camera so every object stays shaded as we fly past */
 S.add(new THREE.HemisphereLight(0xffd6ec,0x2a1060,.58));
 var key=new THREE.DirectionalLight(0xd8d7ff,.62);key.position.set(6,10,8);key.target.position.set(0,0,-12);cam.add(key,key.target);
 var pl1=new THREE.PointLight(0x35e0c2,1.5,70,1);pl1.position.set(-12,4,-10);cam.add(pl1);
 var pl2=new THREE.PointLight(0x8b9bff,1.6,70,1);pl2.position.set(12,-3,-12);cam.add(pl2);
 function gm(o){return new THREE.MeshPhysicalMaterial(Object.assign({metalness:.3,roughness:.26,clearcoat:1,clearcoatRoughness:.12},o||{}))}
 function soft(){var c=document.createElement('canvas');c.width=c.height=128;var x=c.getContext('2d'),g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.4,'rgba(255,255,255,.35)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,128,128);return new THREE.CanvasTexture(c)}
 var ST=soft(),glows=[];
 function glow(sc,op){var s=new THREE.Sprite(new THREE.SpriteMaterial({map:ST,transparent:true,opacity:op,depthWrite:false}));s.scale.set(sc,sc,1);s.userData.op=op;glows.push(s);return s}
 /* camera flight path */
 var path=new THREE.CatmullRomCurve3([[0,4,26],[3,4,6],[-6,5,-22],[7,3,-52],[-7,6,-84],[6,3,-116],[-4,5,-148],[0,3,-182],[0,3,-215]].map(function(p){return new V3(p[0],p[1],p[2])}));
 var tmp=new V3(),tan=new V3(),tgt=new V3(),t2=new V3();
 /* hero piece: faceted crystal, solid rings, orbiting spheres */
 var core=new THREE.Group(),crystal=new THREE.Mesh(new THREE.IcosahedronGeometry(5.2,0),gm({flatShading:true,metalness:.55,roughness:.2})),
  ringA=new THREE.Mesh(new THREE.TorusGeometry(8.6,.5,32,140),gm({metalness:.75,roughness:.22})),
  ringB=new THREE.Mesh(new THREE.TorusGeometry(11.4,.32,32,140),gm({metalness:.7,roughness:.25})),sats=[],halo=glow(34,.5);
 core.add(crystal,ringA,ringB,halo);
 for(var i=0;i<4;i++){var sa=new THREE.Mesh(new THREE.SphereGeometry(.85+i*.12,40,28),gm({metalness:.2,roughness:.18}));core.add(sa);sats.push(sa)}
 core.position.set(13,0,-12);S.add(core);
 /* subject cubes along the path */
 var cubeDark=['#071a33','#092b24','#321316'],cubeAccent=['#38aaff','#32d18b','#ff5964'],cubeMats=[];
 function label(t,i){var c=document.createElement('canvas');c.width=c.height=256;var x=c.getContext('2d');
  x.fillStyle=cubeDark[i%3];x.fillRect(0,0,256,256);
  var ac=cubeAccent[i%3];x.fillStyle=ac;x.globalAlpha=.9;x.fillRect(0,0,256,12);x.globalAlpha=1;x.textAlign='center';x.textBaseline='middle';x.font='700 '+(t.length>5?38:t.length>3?58:78)+'px sans-serif';x.fillStyle='#f4fbff';x.fillText(t,128,132);
  var tx=new THREE.CanvasTexture(c);tx.anisotropy=4;return tx}
 var cubes=[];
 SUBJCODES.forEach(function(s,i){var n=i%3,mat=new THREE.MeshStandardMaterial({map:label(s,i),color:0xffffff,metalness:.38,roughness:.3,emissive:new THREE.Color(cubeDark[n]),emissiveIntensity:.2});cubeMats.push({mat:mat,accent:cubeAccent[n]});var m=new THREE.Mesh(new THREE.BoxGeometry(3.3,3.3,3.3),mat);
  m.add(glow(10,.2));path.getPointAt(.24+i*.04,tmp);var sd=i%2?1:-1;m.position.set(tmp.x+sd*(9+i%3*2),tmp.y+(i%4-1.5)*2.4,tmp.z);m.userData.y0=m.position.y;S.add(m);cubes.push(m)});
 /* scattered gems and spheres */
 var NG=lo?28:60,NB=lo?14:28,gems=new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1,0),new THREE.MeshStandardMaterial({flatShading:true,metalness:.4,roughness:.3}),NG),
  balls=new THREE.InstancedMesh(new THREE.SphereGeometry(1,28,20),new THREE.MeshStandardMaterial({metalness:.25,roughness:.22}),NB),gd=[],bd=[],dm=new THREE.Object3D();
 function scatter(arr,n,rmin,rv,smin,sv){for(var i=0;i<n;i++){path.getPointAt(.13+Math.random()*.84,tmp);var an=Math.random()*6.283,rd=rmin+Math.random()*rv,dx=Math.cos(an)*rd;if(tmp.z>-70&&Math.abs(dx)<16)dx=(dx<0?-1:1)*(16+Math.random()*8);arr.push({x:tmp.x+dx,y:tmp.y+Math.sin(an)*rd*.6,z:tmp.z+(Math.random()-.5)*8,r:.2+Math.random()*.7,s:smin+Math.random()*sv,p:Math.random()*6.28})}}
 scatter(gd,NG,11,16,.5,1.1);scatter(bd,NB,12,18,.7,1.3);S.add(gems,balls);
 /* dust */
 var ND=lo?260:600,dp=new Float32Array(ND*3);for(i=0;i<ND;i++){dp[i*3]=(Math.random()-.5)*90;dp[i*3+1]=(Math.random()-.5)*50+4;dp[i*3+2]=40-Math.random()*270}
 var dg=new THREE.BufferGeometry();dg.setAttribute('position',new THREE.BufferAttribute(dp,3));var dust=new THREE.Points(dg,new THREE.PointsMaterial({map:ST,size:.55,transparent:true,opacity:.55,depthWrite:false,sizeAttenuation:true}));S.add(dust);
 /* far-field light blooms for depth */
 var blooms=[];for(i=0;i<7;i++){path.getPointAt(.14+i*.12,tmp);var b=glow(60+Math.random()*40,.2);b.position.set(tmp.x+(i%2?1:-1)*(22+Math.random()*10),tmp.y+(Math.random()-.3)*10,tmp.z-10);S.add(b);blooms.push(b)}
 /* finale: large crystal cluster */
 var fin=new THREE.Group(),f1=new THREE.Mesh(new THREE.IcosahedronGeometry(6.5,0),gm({flatShading:true,metalness:.55,roughness:.2})),f2=new THREE.Mesh(new THREE.TorusGeometry(10.5,.5,32,140),gm({metalness:.75,roughness:.22})),f3=new THREE.Mesh(new THREE.SphereGeometry(2,40,28),gm());
 fin.add(f1,f2,f3,glow(46,.5));f3.position.set(10,-4,2);path.getPointAt(1,tmp);path.getTangentAt(1,tan);fin.position.copy(tmp).addScaledVector(tan,34);fin.position.x+=9;S.add(fin);
 var pal=[],objPal=[];
 onTheme=function(){var bg=col('--bg'),a=col('--a'),b=col('--b'),c=col('--c'),lt=root.dataset.theme==='light';pal=[a,b,c,col('--a2')];
  objPal=lt
   ? [new THREE.Color('#1f5d47'),new THREE.Color('#a86728'),new THREE.Color('#874735'),new THREE.Color('#6d7a47')]
   : [new THREE.Color('#174a3a'),new THREE.Color('#9a5d22'),new THREE.Color('#71372c'),new THREE.Color('#3f6546')];
  S.fog.color.copy(bg);crystal.material.color.copy(objPal[0]);ringA.material.color.copy(objPal[1]);ringB.material.color.copy(objPal[2]);f1.material.color.copy(objPal[0]);f2.material.color.copy(objPal[1]);f3.material.color.copy(objPal[2]);
  sats.forEach(function(s,i){s.material.color.copy(objPal[(i+1)%4])});
  for(var k=0;k<NG;k++)gems.setColorAt(k,objPal[k%4]);gems.instanceColor.needsUpdate=true;for(k=0;k<NB;k++)balls.setColorAt(k,objPal[(k+1)%4]);balls.instanceColor.needsUpdate=true;
  dust.material.color.copy(lt?a:b);dust.material.opacity=lt?.35:.55;dust.material.blending=lt?THREE.NormalBlending:THREE.AdditiveBlending;dust.material.needsUpdate=true;
  glows.forEach(function(g,i){g.material.color.copy(objPal[i%3]);g.material.blending=lt?THREE.NormalBlending:THREE.AdditiveBlending;g.material.opacity=lt?g.userData.op*.24:g.userData.op*.42;g.material.needsUpdate=true});
  cubeMats.forEach(function(v,i){v.mat.color.copy(objPal[i%4]);v.mat.emissive.copy(objPal[i%4]);v.mat.emissiveIntensity=lt?.1:.16;v.mat.needsUpdate=true});
  pl1.color.copy(objPal[1]);pl2.color.copy(objPal[0]);R.toneMappingExposure=lt?.88:.94};
 onTheme();
 function size(){R.setSize(innerWidth,innerHeight,false);cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix()}addEventListener('resize',size);size();
 addEventListener('pointermove',function(e){mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5},{passive:true});
 var sm=0,pv=0,vs=0,mxs=0,mys=0,clk=new THREE.Clock();
 (function loop(){requestAnimationFrame(loop);if(!document.body.classList.contains('app'))return;var d=Math.min(clk.getDelta(),.05),t=RM?0:clk.elapsedTime,max=Math.max(1,document.documentElement.scrollHeight-innerHeight),tp=clamp(typeof api.source==='function'?api.source():scrollY/max,0,1);
  sm=RM?tp:lerp(sm,tp,1-Math.pow(.004,d));vs=lerp(vs,Math.abs(sm-pv)/Math.max(d,.001),.12);pv=sm;SP=sm;var u=clamp(sm,0,1);mxs=lerp(mxs,mx,.06);mys=lerp(mys,my,.06);
  path.getPointAt(u,tmp);path.getTangentAt(u,tan);path.getTangentAt(Math.min(1,u+.04),t2);
  cam.position.set(tmp.x+mxs*2.6,tmp.y-mys*1.6,tmp.z);tgt.copy(tmp).addScaledVector(tan,30);tgt.x+=mxs*7;tgt.y+=-mys*4+1;cam.lookAt(tgt);cam.rotateZ(clamp(-mxs*.05+(t2.x-tan.x)*1.6,-.25,.25));
  cam.fov=lerp(cam.fov,55+(RM?0:clamp(vs*30,0,8)),.12);cam.updateProjectionMatrix();
  core.rotation.y=t*.18+mxs*.6;core.rotation.x=t*.08+mys*.4;crystal.rotation.y=t*.3;ringA.rotation.x=t*.22;ringA.rotation.y=.6;ringB.rotation.y=t*.16;ringB.rotation.x=1.1;
  sats.forEach(function(s,i){var a=t*(.45+i*.14)+i*1.6,r=7.4+i*1.2;s.position.set(Math.cos(a)*r,Math.sin(a*.8+i)*r*.4,Math.sin(a)*r)});
  cubes.forEach(function(m,i){m.rotation.y=t*.3+i;m.rotation.x=Math.sin(t*.4+i)*.25;m.position.y=m.userData.y0+Math.sin(t*.8+i)*.6});
  gd.forEach(function(v,k){dm.position.set(v.x,v.y+Math.sin(t*.6+v.p)*.8,v.z);dm.rotation.set(t*v.r+v.p,t*v.r*.7,0);dm.scale.setScalar(v.s);dm.updateMatrix();gems.setMatrixAt(k,dm.matrix)});gems.instanceMatrix.needsUpdate=true;
  bd.forEach(function(v,k){dm.position.set(v.x,v.y+Math.sin(t*.5+v.p)*1,v.z);dm.rotation.set(0,0,0);dm.scale.setScalar(v.s);dm.updateMatrix();balls.setMatrixAt(k,dm.matrix)});balls.instanceMatrix.needsUpdate=true;
  dust.position.y=Math.sin(t*.2)*.8;fin.rotation.y=t*.2;f1.rotation.x=t*.15;f2.rotation.x=t*.2;f2.rotation.y=.5;
  R.render(S,cam)})();
}

Object.defineProperty(api,'progress',{get:function(){return SP}});
})();
