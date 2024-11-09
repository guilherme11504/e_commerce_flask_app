document.getElementById('eatHereBtn').addEventListener('click', function() {
    localStorage.setItem('orderType', 'comerAqui');
    window.location.href = '/client_menu';
});

document.getElementById('takeAwayBtn').addEventListener('click', function() {
    localStorage.setItem('orderType', 'levar');
    window.location.href = '/client_menu';
});
