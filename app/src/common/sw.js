const CACHE_NAME = '__CACHE_NAME__';
const OFFLINE_PAGE = '/offline.html';

const ESSENTIAL_ASSETS = [
    OFFLINE_PAGE,
    '/favicon.png',
    '/'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ESSENTIAL_ASSETS))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => caches.match(OFFLINE_PAGE))
        );
    } else {
        event.respondWith(
            caches.match(event.request)
                .then(response => response || fetch(event.request))
                .catch(() => {
                    if (event.request.destination === 'document') {
                        return caches.match(OFFLINE_PAGE);
                    }
                })
        );
    }
}); 
