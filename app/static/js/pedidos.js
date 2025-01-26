document.addEventListener("DOMContentLoaded", () => {
    const pedidos = document.querySelectorAll(".pedido");

    pedidos.forEach(pedido => {
        const dataPedidoEl = pedido.querySelector(".pedido-data");
        const temposPreparosEls = pedido.querySelectorAll(".tempo-preparo");

        // Verifica se a data do pedido está presente
        if (!dataPedidoEl || temposPreparosEls.length === 0) {
            console.error("Faltando dados no pedido:", pedido);
            return;
        }

        // Parse data do pedido
        const dataPedido = new Date(dataPedidoEl.textContent.trim());
        const agora = new Date();

        if (isNaN(dataPedido)) {
            console.error("Data inválida para o pedido:", dataPedidoEl.textContent);
            return;
        }

        // Calcular tempo total de preparo
        let tempoTotalPreparo = 0;
        temposPreparosEls.forEach(el => {
            const tempoPreparo = parseInt(el.textContent.trim(), 10);
            if (!isNaN(tempoPreparo)) {
                tempoTotalPreparo += tempoPreparo;
            } else {
                console.warn("Tempo de preparo inválido:", el.textContent);
            }
        });

        if (tempoTotalPreparo === 0) {
            console.warn("Tempo total de preparo é zero para o pedido:", pedido);
            return;
        }

        // Calcular tempo decorrido em minutos
        const tempoDecorrido = Math.floor((agora - dataPedido) / (1000 * 60)); // Minutos

        // Lógica de cores
        let cor = "";
        if (tempoDecorrido <= tempoTotalPreparo * 0.5) {
            cor = "green"; // Menos da metade do tempo passou
        } else if (tempoDecorrido <= tempoTotalPreparo) {
            cor = "yellow"; // Dentro do tempo estimado
        } else {
            cor = "red"; // Atrasado
        }

        // Aplicar cor ao pedido
        pedido.style.borderColor = cor;
        pedido.style.borderWidth = "3px";
    });
});