$(function (){

    var ip = "localhost";


    $.ajax({
        url: "http://localhost:5000/listar",
        method: "GET",
        dataType: "json",
        success: listar,
        error: function () {
            alert("Erro back-end!")
        }
    });

    function listar(retorno){
        if (retorno.resultado == "ok"){
            for (let d of (retorno.detalhes)){

                var linha = "<tr>" +
                    "<td>" + d.id + "</td>" + 
                    "<td>" + d.score + "</td>" + 
                    "</tr>";
                    $("#scores").append(linha);
            }
        }else{
            alert(retorno.resultado + retorno.detalhes);}
    }
});

$(document).on("click", "refresh", function(){
    location.reload()
});
