//Cooredenadas entrega
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        document.getElementById('final_lat').value = position.coords.latitude;
        document.getElementById('final_lng').value = position.coords.longitude;
    });
}
//coordenadas insucesso
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position2) {
        document.getElementById('final_lat2').value = position2.coords.latitude;
        document.getElementById('final_lng2').value = position2.coords.longitude;
    });
}



// Scrip que lida com os cards do app SAC e Frota
document.addEventListener("DOMContentLoaded", function() {
    var cards = document.querySelectorAll('.clickable-card');
    cards.forEach(function(card) {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {  
                window.location.href = card.getAttribute('data-url');
            }
        });
    });
});
$(document).ready(function() {
    $('.clickable-card').on('click', function(e) {
        if (!$(e.target).closest('a').length) {  
            window.location.href = $(this).data('url');
        }
    });
});
// $('.card-checkbox').on('click', function(e) {
//     e.stopPropagation(); 
// });
$('.card-header').on('click', function(e) {
    e.stopPropagation(); 
});

document.getElementById("selectAllCheckbox").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll("input[name='selected_ent']");
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

document.getElementById("selectAllCheckbox").addEventListener("change", function() {
    var checkboxes = document.querySelectorAll("input[name='selected_contacts']");
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});
// Script que lida finalização do SAC


function confirmCompletion(event) {
    event.preventDefault(); 

    var form = event.target.form;

    // Exibir um diálogo de confirmação
    var confirmMessage = "Deseja realmente concluir este SAC?";
    if (confirm(confirmMessage)) {
        form.submit(); 
    }
}


  document.getElementById('fileInput').addEventListener('change', function(e) {
    var fileName = e.target.files[0].name;
    document.getElementById('fileName').textContent = "Arquivo selecionado: " + fileName;
});




function showModal() {
    document.querySelector('.modal-backdrop').style.display = 'block';
    document.querySelector('.modal').style.display = 'block';
}
// function closeModal2() {
//     document.getElementById("FinalizaModal").style.display = "none";
// }
function closeModal2(event) {
    if (event) {
        event.stopPropagation();
    }
    document.getElementById("FinalizaModal").style.display = "none";
}

function closeModal() {
    document.querySelector('.modal-backdrop').style.display = 'none';
    document.querySelector('.modal').style.display = 'none';
}
function closeModal() {
    document.getElementById("insucessoModal").style.display = "none";
}

function confirmEntrega(event) {
    event.preventDefault();
    showModal();
}



// function showInsucessoModal(event) {
//     event.preventDefault();
//     document.getElementById("insucessoModal").style.display = "block";
// }

// function submitInsucessoForm() {
//     document.querySelector("#insucessoModal form").submit();
// }

function showInsucessoModal() {
    document.querySelector('.modal-backdrop').style.display = 'block';
    document.getElementById('insucessoModal').style.display = 'block';
}

function closeModal() {
    document.querySelector('.modal-backdrop').style.display = 'none';
    document.getElementById('insucessoModal').style.display = 'none';
}

function submitInsucessoForm(actionType) {
    document.getElementById('actionTypeInput').value = actionType;
}






document.addEventListener("DOMContentLoaded", function() {
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(setPosition);
        } else {
            alert("A geolocalização não é suportada por este navegador.");
        }
    }

    function setPosition(position) {
        let lat = position.coords.latitude;
        let lng = position.coords.longitude;
        document.getElementById("starting_point_lat").value = lat;
        document.getElementById("starting_point_lng").value = lng;
    }

    getLocation();
});

