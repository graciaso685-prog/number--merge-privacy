// Glimmer Maze a déménagé vers /glimmer-maze/.
// Cette version du service worker s'efface elle-même et renvoie les joueurs vers la nouvelle adresse.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('glimmer-maze-')) await caches.delete(k);
    await self.registration.unregister();
    for (const c of await self.clients.matchAll({ type: 'window' })) c.navigate('/glimmer-maze/');
  })());
});
