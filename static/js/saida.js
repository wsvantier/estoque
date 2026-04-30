const selectProduto = document.getElementById('select_produto');
const selectCategoria = document.getElementById('categoria');
const limite = document.getElementById('quantidade');

// Quando muda a categoria → carrega produtos
selectCategoria.addEventListener('change', async function() {
    const categoriaId = this.value;
    
    try {
        const response = await fetch(`/saida/api/categoria/${categoriaId}`);
        const dados = await response.json();

        selectProduto.innerHTML = '<option value="" disabled selected> -- Selecione -- </option>';

        dados.forEach(item => {
            const novaOpcao = new Option(`${item.nome} - Disponível: ${item.quantidade}${item.medida} - Validade: ${item.validade}`, item.id);
            novaOpcao.dataset.produtoId = item.id;
            novaOpcao.dataset.quantidade = item.quantidade;
            selectProduto.add(novaOpcao);
        });

    } catch (error) {
        console.error("Erro ao buscar produtos:", error);
    }
    limite.value = ''
    limite.max = 0
});

selectProduto.addEventListener("change", function(){

    const selecionado = this.options[this.selectedIndex];
    const quantidade =  selecionado.dataset.quantidade;
    limite.value = ''
    limite.max = quantidade;


})
