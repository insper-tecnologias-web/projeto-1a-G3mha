function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener("DOMContentLoaded", function () {
  // Faz textarea aumentar a altura automaticamente
  // Fonte: https://www.geeksforgeeks.org/how-to-create-auto-resize-textarea-using-javascript-jquery/#:~:text=It%20can%20be%20achieved%20by,height%20of%20an%20element%20automatically.
  let textareas = document.getElementsByClassName("autoresize");
  for (let i = 0; i < textareas.length; i++) {
    let textarea = textareas[i];
    function autoResize() {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    }

    textarea.addEventListener("input", autoResize, false);
  }

  // Sorteia classes de cores aleatoriamente para os cards
  let cards = document.getElementsByClassName("card");
  for (let i = 0; i < cards.length; i++) {
    let card = cards[i];
    card.className += ` card-color-${getRandomInt(
      1,
      5
    )} card-rotation-${getRandomInt(1, 11)}`;
  }
});

function refreshNote(button){
  let doc = button.parentElement.parentElement;
  // pega os values originais
  let previous_title = doc.children[1];
  let previous_details = doc.children[2].children[1];
  // pega os values editados
  let new_title = doc.children[0];
  let new_details = doc.children[2].children[0];
  // cria elementos input
  let prev_ttl = document.createElement('input');
  let prev_dtl = document.createElement('input');
  // atribui name e o value de cada input criado
  prev_ttl.value = previous_title.value;
  prev_dtl.value = previous_details.value;
  prev_ttl.name = 'prev_ttl';
  prev_dtl.name = 'prev_dtl';
  // seta atributo hidden para não ser exibido
  prev_ttl.setAttribute('type', 'hidden');
  prev_dtl.setAttribute('type', 'hidden');
  // adiciona os inputs ao doc
  doc.appendChild(prev_ttl);
  doc.appendChild(prev_dtl);
  // atribui os novos values
  previous_title.value = new_title.innerHTML;
  previous_details.value = new_details.innerHTML;
}

document.querySelectorAll('h3, p').forEach((node) => { // para editar cada h3 e p
  node.ondblclick = function(){ // ao clicar duas vezes
    let conteudo = this.innerHTML; // recebe o conteudo do elemento clicado
    // cria um inpu que recebe o conteudo
    let input = document.createElement('Input'); // cria um input
    input.conteudo = conteudo; // atribui o conteudo ao input
    input.onblur = function() { // usuario clica fora do input
        this.parentNode.innerHTML = this.conteudo; // insere o conteudo substituindo o anterior
    }
    // limpa o conteúdo e adiciona o input
    this.innerHTML = ''; // limpa onde conteudo esta armazenado
    this.appendChild(input); // adiciona o input
    input.focus(); // coloca o cursor no input
  }
});