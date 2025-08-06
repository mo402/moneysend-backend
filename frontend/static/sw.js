self.addEventListener('install', e => {
  console.log('Service worker installé');
  e.waitUntil(
    caches.open('money-cache').then(cache => {
      return cache.addAll([
        '/',
        '/static/manifest.json',
        '/static/icons/icon-192.png'
      ]);
    })
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(response => response || fetch(e.request))
  );
});
