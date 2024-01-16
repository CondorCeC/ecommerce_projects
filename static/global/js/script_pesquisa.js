function showInfo(rating) {
  var infoElement = document.getElementById('info');
  var infoText = '';

  switch (rating) {
    case 'excelente':
      infoText = `
      <p><i>Quais foram as características que mais chamaram atenção?</i></p>
      <ul>
        
        <li><input type="checkbox" name="options[]" value="Agilidade da Entrega"> Agilidade da entrega</li>
        <li><input type="checkbox" name="options[]" value="Agilidade da Retirada"> Agilidade da retirada</li>
        <li><input type="checkbox" name="options[]" value="Disponibilidade de Produtos"> Disponibilidade de produtos</li>
        <li><input type="checkbox" name="options[]" value="Facilidade de Compra no site"> Facilidade de compra no site</li>
        <li><input type="checkbox" name="options[]" value="Qualidade da Separação"> Qualidade da separação</li>
        <li><input type="checkbox" name="options[]" value="Superou as Expectativas"> Superou as expectativas</li>
      </ul>
      `;
      break;

    case 'bom':
      infoText = `
      <p><i>Quais foram as características que mais chamaram atenção?</i></p>  
      <ul>
            <li><input type="checkbox" name="options[]" value="Atendimento na Loja"> Atendimento na loja</li>
            <li><input type="checkbox" name="options[]" value="Escolha da Carne"> Escolha da carne</li>
            <li><input type="checkbox" name="options[]" value="Escolha das Frutas"> Escolha do hortifrúti</li>
            <li><input type="checkbox" name="options[]" value="Formas de Pagamento"> Formas de pagamento</li>
            <li><input type="checkbox" name="options[]" value="Mais opções de produtos no site"> Mais opções de produtos no site</li>
            <li><input type="checkbox" name="options[]" value="Não substituíram produtos"> Não substituíram produtos</li>
            <li><input type="checkbox" name="options[]" value="Substituíram produtos sem minha autorização"> Substituíram produtos sem minha autorização</li>
            <li><input type="checkbox" name="options[]" value="Serviço de Entrega"> Serviço de entrega</li>
            <li><input type="checkbox" name="options[]" value="Temperatura dos Produtos"> Temperatura dos produtos</li>
            <li><input type="checkbox" name="options[]" value="Validade dos Produtos"> Validade dos produtos</li>
        </ul>
      `;
      break;

    case 'okay':
    case 'ruim':
    case 'pessimo':
      infoText = `
      <p><i>Quais as características do pedido que influenciaram sua decisão?</i></p>  
      <ul>
            <li><input type="checkbox" name="options[]" value="Atendimento do Entregador"> Atendimento do entregador</li>
            <li><input type="checkbox" name="options[]" value="Atendimento na Loja"> Atendimento na loja</li>
            <li><input type="checkbox" name="options[]" value="Entrega Fora do Horário"> Entrega fora do horário</li>
            <li><input type="checkbox" name="options[]" value="Não recebi todos os produtos do meu pedido"> Não recebi todos os produtos</li>
            <li><input type="checkbox" name="options[]" value="Substituíram produtos sem minha autorização"> Substituíram produtos sem minha autorização</li>
            <li><input type="checkbox" name="options[]" value="Separação Ruim dos Produtos"> Separação ruim dos produtos</li>
            <li><input type="checkbox" name="options[]" value="Escolha do hortifruti"> Escolha do hortifruti</li>
            <li><input type="checkbox" name="options[]" value="Escolha da carne"> Escolha da carne</li>
            <li><input type="checkbox" name="options[]" value="Temperatura dos Produtos"> Temperatura dos produtos</li>
            <li><input type="checkbox" name="options[]" value="Validade dos Produtos"> Validade dos produtos</li>
            <li><input type="checkbox" name="options[]" value="Mais formas de pagamento"> Mais formas de pagamento</li>
            <li><input type="checkbox" name="options[]" value="Dificuldade de compra no site"> Dificuldade de compra no site</li>
            <li><input type="checkbox" name="options[]" value="Dificuldade na retirada"> Dificuldade na retirada</li>

        </ul>
      `;
      break;
  }

  infoElement.innerHTML = infoText;
}

function validarFormulario() {
  var radios = document.getElementsByName("rating");
  var selecionado = false;

  for (var i = 0; i < radios.length; i++) {
    if (radios[i].checked) {
      selecionado = true;
      break;
    }
  }

  if (!selecionado) {
    var alerta = document.createElement("div");
    alerta.classList.add("alert");
    alerta.textContent = "Por favor, selecione uma opção de avaliação.";

    var formulario = document.getElementById("pesquisa");
    formulario.insertBefore(alerta, formulario.firstChild);

    return false; // Impede o envio do formulário
  }

  return true; // Permite o envio do formulário
}

document.getElementById("pesquisa").addEventListener("submit", function(event) {
  if (!validarFormulario()) {
    event.preventDefault(); // Impede o envio do formulário
  }
});