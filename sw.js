// Service worker mínimo: permite instalar la web como app y abrirla sin conexión.
// Solo guarda la página y los archivos de la app; imágenes y demás pasan directo a la red.
var CACHE = 'rowling-v1';
var SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png'];
self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){ return c.addAll(SHELL); }).then(function(){ return self.skipWaiting(); }));
});
self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(ks){ return Promise.all(ks.filter(function(k){return k !== CACHE;}).map(function(k){return caches.delete(k);})); }).then(function(){ return self.clients.claim(); }));
});
self.addEventListener('fetch', function(e){
  var r = e.request, u = new URL(r.url);
  if(r.method !== 'GET' || u.origin !== location.origin) return;
  var name = u.pathname.split('/').pop();
  var isShell = r.mode === 'navigate' || name === '' || SHELL.indexOf(name) > -1;
  if(!isShell) return;
  e.respondWith(
    fetch(r).then(function(res){
      var copy = res.clone();
      caches.open(CACHE).then(function(c){ c.put(r, copy); });
      return res;
    }).catch(function(){ return caches.match(r).then(function(m){ return m || caches.match('index.html'); }); })
  );
});
