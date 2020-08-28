let fieldNamesDecode = {
    Login: "Логин",
    Ident: "Идентификатор"
};
let shuffledAlf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!',  ';', '%', ':',  '@', '*', '(', ')', '_', '+', '=']
                                .sort(function(){ return Math.random() - 0.5; }).join("");
console.log(shuffledAlf);


function showMsg(msg, kind,  sucFunc=function () {}, field="") {
    switch (kind) {
        case "Suc":
            jq("#psyFormBtnSave").prop("disabled", true);
            jq("#psyFormSignSuc").fadeIn(1000).delay(3000).fadeOut(500);
            sucFunc();
            return;
        case "DuplicatedField":
            let capitalizedField = field.replace(/(^|\s)\S/g, l => l.toUpperCase());
            jq(`#psyForm${capitalizedField}`).toggleClass("is-invalid", true);
            jq(`#psyForm${capitalizedField}Msg`).text(`Такой ${fieldNamesDecode[capitalizedField]} уже существует`);
            return;
        default:
            jq("#fatalMsg").text(msg?msg:"Произошла неизвестная ошибка").fadeIn(700).delay(6000).fadeOut(4000);
    }

}



function generatePas(len){
    let pas = "";
    for (let i=0; i<len; i++){
        pas += shuffledAlf.charAt(Math.floor(Math.random() * shuffledAlf.length));
    }
    return pas;
}