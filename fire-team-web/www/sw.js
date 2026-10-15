// Fire Team PWA service worker
// Bump CACHE_VERSION whenever you change the app to force clients to update.
const CACHE_VERSION = 'fireteam-v8';
// Everything the app needs runs locally, so caching these makes it fully offline.
const APP_SHELL = [
  '/',
  '/engine.js',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/static/apple-touch-icon.png',
  '/manifest.webmanifest'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  // Navigations: network-first so updates land, cache fallback offline.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE_VERSION).then((c) => c.put('/', copy));
          return resp;
        })
        .catch(() => caches.match('/'))
    );
    return;
  }

  // The engine changes together with the page, so fetch it network-first too.
  if (new URL(request.url).pathname === '/engine.js') {
    event.respondWith(
      fetch(request)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE_VERSION).then((c) => c.put(request, copy));
          return resp;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // Static assets: cache-first.
  event.respondWith(
    caches.match(request).then((cached) => cached || fetch(request).then((resp) => {
      const copy = resp.clone();
      caches.open(CACHE_VERSION).then((c) => c.put(request, copy));
      return resp;
    }))
  );
});
