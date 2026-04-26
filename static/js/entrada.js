


const selectCategoria = document.getElementById('cat'); // Select da categoria
const selectProduto = document.getElementById('produto'); // Aonde vai ser inserido os dados

async function CarregarCategorias(){

    const categoria = selectCategoria.value; // Valor do itens do Select

    const response = await fetch(`/entrada/api/produtos/${categoria}`);
    const dados = await response.json();

    // Limpa opções antigas
    selectProduto.innerHTML = '<option value="" disabled selected> -- Selecione -- </option>';

    dados.forEach(item => {
        const novaOpcao = new Option(item.nome, item.id);
        selectProduto.add(novaOpcao);
    });
}

// Evento 
selectCategoria.addEventListener('change', CarregarCategorias);