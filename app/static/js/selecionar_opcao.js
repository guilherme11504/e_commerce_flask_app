function nextScreen() {
    var comerAqui = document.getElementById('eatHereBtn');
    var viagem = document.getElementById('takeAwayBtn');
    var orderType = null;
    
    // Altera a visibilidade dos botões
    comerAqui.style.display = 'none';
    viagem.style.display = 'none';
    
    // Verifica se comerAqui ou viagem possuem a classe selected
    if (comerAqui.classList.contains('selected')) {
        orderType = 'balcao';
    } else if (viagem.classList.contains('selected')) {
        orderType = 'viagem';
    } else {
        alert('Selecione uma opção');
        return; // Impede o fluxo se nenhuma opção foi selecionada
    }
    
    var cliente_nome = document.getElementById('clientName').value;

    localStorage.setItem('orderType', orderType);
    localStorage.setItem('clientName', cliente_nome);
    

    window.location.href = '/client_menu';
}
