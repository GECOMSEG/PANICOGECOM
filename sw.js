// sw.js — GECOM Notificações em segundo plano
self.addEventListener('install', e => self.skipWaiting())
self.addEventListener('activate', e => e.waitUntil(clients.claim()))

// Recebe notificação e mostra mesmo fechado
self.addEventListener('push', e => {
  const dados = e.data?.json() || { titulo: 'GECOM', mensagem: 'Nova notificação' }
  self.registration.showNotification(dados.titulo, {
    body: dados.mensagem,
    icon: 'https://via.placeholder.com/192/FF0000/FFFFFF?text=G',
    badge: 'https://via.placeholder.com/72/FF0000/FFFFFF?text=G',
    vibrate: [200, 100, 200],
    data: { url: '/' }
  })
})

// Ao clicar na notificação
self.addEventListener('notificationclick', e => {
  e.notification.close()
  e.waitUntil(clients.openWindow(e.notification.data.url))
})
