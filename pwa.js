if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

function subscribe() {
  navigator.serviceWorker.ready.then(function(registration) {
    return Notification.requestPermission()
      .then(function(premission) {
        if (premission !== 'denied') {
          return registration.pushManager.subscribe({ userVisibleOnly: true })
            .then(function(s) {
              return fetch('/push', {
                method: 'post',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'endpoint=' + s.endpoint
                  + '&p256dh=' + btoa(String.fromCharCode.apply(null, new Uint8Array(s.getKey('p256dh')))).replace(/\+/g, '-').replace(/\//g, '_')
                  + '&auth=' + btoa(String.fromCharCode.apply(null, new Uint8Array(s.getKey('auth')))).replace(/\+/g, '-').replace(/\//g, '_')
              });
            });
        }
      });
  });
}
