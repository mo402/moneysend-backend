self.addEventListener("install", (e) => {
  console.log("Service Worker installé");
  e.waitUntil(
    caches.open("moneysend-cache").then((cache) => {
      return cache.addAll(["/", "/static/style.css"]);
    })
  );
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((res) => {
      return res || fetch(e.request);
    })
  );
});
