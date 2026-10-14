self.addEventListener('push', function(event) {
    const data = event.data ? event.data.json() : { title: '新しい連絡', body: '掲示板が更新されました！' };
    
    const options = {
        body: data.body,
        icon: '/static/icon.png',
        badge: '/static/icon.png',
        vibrate: [100, 50, 100]
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});
