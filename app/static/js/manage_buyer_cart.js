
        let cart = [];
        let total = 0;
        let selectedProduct = {};

        document.addEventListener("DOMContentLoaded", () => {
    // Seleciona todos os botões de "Adicionar ao Carrinho"
    const buttons = document.querySelectorAll(".add-to-cart-button");

    // Adiciona evento de clique a todos os botões
    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const hash = button.getAttribute("data-hash");
            const nome = button.getAttribute("data-nome");
            const preco = parseFloat(button.getAttribute("data-preco"));
            const items = JSON.parse(button.getAttribute("data-items")); // Converte JSON string para array

            // Chama a função para exibir o modal do produto
            showProductModal(hash, nome, preco, items);
        });
    });
});

// Exibir o modal do produto
function showProductModal(id, name, price, editableItems) {
    // Atualiza o produto selecionado
    selectedProduct = { id, name, price, editableItems };

    // Atualiza o nome do produto no modal
    document.getElementById("modalProductName").innerText = name;

    // Limpa o container de itens editáveis
    const itemsContainer = document.getElementById("editableItemsContainer");
    itemsContainer.innerHTML = "";

    // Verifica se editableItems é um array e contém itens
    if (Array.isArray(editableItems) && editableItems.length > 0) {
        editableItems.forEach(item => {
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.id = `edit-${item}`;
            checkbox.name = item;

            const label = document.createElement("label");
            label.htmlFor = `edit-${item}`;
            label.innerText = item;

            itemsContainer.appendChild(checkbox);
            itemsContainer.appendChild(label);
            itemsContainer.appendChild(document.createElement("br"));
        });
    } else {
        // Adiciona mensagem quando não há itens editáveis
        const message = document.createElement("p");
        message.innerText = "Nenhum item editável disponível para este produto.";
        itemsContainer.appendChild(message);
    }

    // Garante que o modal seja exibido
    const modalElement = document.getElementById('productModal');
    const productModal = new bootstrap.Modal(modalElement, { keyboard: true });
    productModal.show();
}

// Função para adicionar produto ao carrinho
function addToCart() {
    const quantity = parseInt(document.getElementById("quantity").value);
    const totalItemPrice = selectedProduct.price * quantity;
    // Seleciona os itens editáveis marcados
    const selectedEditableItems = [];
    const checkboxes = document.querySelectorAll('#editableItemsContainer input[type="checkbox"]:checked');
    checkboxes.forEach(checkbox => {
        selectedEditableItems.push(checkbox.name);
    });

    // Adiciona os itens selecionados ao carrinho
    const cartItem = {
        ...selectedProduct,
        quantity,
        price: totalItemPrice,
        editableItems: selectedEditableItems, // Apenas os itens editáveis selecionados
    };

    // Adiciona o produto ao carrinho
    cart.push(cartItem);
    total += totalItemPrice;

    updateCart();
    bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
}



        // Atualiza o conteúdo do carrinho e exibe o total
        function updateCart() {
            const cartItemsContainer = document.getElementById("cartItems");
            cartItemsContainer.innerHTML = "";
            document.getElementById("cartTotal").innerText = total.toFixed(2);
            document.getElementById("cart-count").innerText = cart.length;

            cart.forEach((item, index) => {
                const itemDiv = document.createElement("div");
                itemDiv.className = "cart-item";
                itemDiv.innerHTML = `
                    <div>
                        <strong>${item.name}</strong>
                        <span class="text-muted"> - R$ ${item.price.toFixed(2)} (Qtd: ${item.quantity})</span>
                        <button class="btn btn-sm btn-danger" onclick="removeFromCart(${index})">Remover</button>
                    </div>`;
                cartItemsContainer.appendChild(itemDiv);
            });
        }

        // Função para remover item do carrinho
        function removeFromCart(index) {
            total -= cart[index].price;
            cart.splice(index, 1);
            updateCart();
        }

        // Exibir/ocultar a sidebar do carrinho
        function toggleCart() {
            const cartSidebar = document.getElementById("cartSidebar");
            cartSidebar.classList.toggle("d-none");
        }

        // Função para definir o tipo de pedido
        function set_order_type() {
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
        
            localStorage.setItem('orderType', orderType);
        }

        // Simulação do checkout
        function checkout() {
            if (cart.length === 0) {
                alert("O carrinho está vazio!");
                return;
            }

            //pega o id do vendedor do input hidden
            const vendedor_id = document.getElementById("vendedor_id").value;

            if(sessionStorage.getItem('user_type') == 'buyer'){
                set_order_type();
            }
            //captura o texto do textarea do id observacoes
            const observacoes = document.getElementById("observacoes").value;


            // Envia a requisição para o backend
            fetch('/api/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    products: cart,
                    total: total,
                    order_type: localStorage.getItem('orderType'),
                    client_name: localStorage.getItem('clientName'),
                    observacoes: observacoes,
                    vendedor_id:vendedor_id
                })
            })
                .then(response => {
                    if (response.status === 201) {
                        return response.json();
                    } else {
                        throw new Error(`Erro ao realizar o pedido: ${response.status}`);
                    }
                })
                .then(data => {
                    console.log(data);
                    alert('Pedido realizado com sucesso!');
                })
                .catch(error => {
                    console.error('Erro no checkout:', error);
                    alert('Houve um problema ao realizar o pedido. Tente novamente.');
                });
            localStorage.removeItem('orderType');
            localStorage.removeItem('clientName');
            cart = [];
            total = 0;
            updateCart();
            toggleCart();
            window.location.href = '/totem_home';
        }
        document.addEventListener('DOMContentLoaded', function() {
            const buttons = document.querySelectorAll('.optionBtn');
            buttons.forEach(button => {
                button.addEventListener('click', function() {
                    buttons.forEach(btn => btn.classList.remove('selected'));
                    this.classList.add('selected');
                });
            });
        });