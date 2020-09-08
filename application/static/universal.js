let lastKey;

let fieldNamesDecode = {
    Login: "Логин",
    Ident: "Идентификатор"
};
let resultDecode = {};
resultDecode["Нет результата"] = ["not_yet", "secondary"];
resultDecode["Рискует"] = ["clear", "success"];
resultDecode["Не рискует"] = ["danger", "danger"];


let shuffledAlf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!',  ';', '%', ':',  '@', '(', ')', '_', '=']
                                .sort(function(){ return Math.random() - 0.5; }).join("");


function showMsg(msg, kind,  sucFunc=function () {}, field="") {
    switch (kind) {
        case "Good":  sucFunc(); return;
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
        case "Fatal":
            jq("#fatalMsg").text("Ошибка: "+msg).fadeIn(700).delay(6000).fadeOut(4000);
            return;
        default:
            jq("#fatalMsg").text("Произошла неизвестная ошибка").fadeIn(700).delay(6000).fadeOut(4000);
    }

}


function sort(list, key) {
    if (key) {
        if (key === lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }

        list.sort(function (a, b) {
            if (a[key] > b[key]) { return reverse; }
            if (a[key] < b[key]) { return -1*reverse; }
            return 0;
        });
    }
    return list;

}



function generatePas(len){
    let pas = "";
    for (let i=0; i<len; i++){
        pas += shuffledAlf.charAt(Math.floor(Math.random() * shuffledAlf.length));
    }
    return pas;
}


function stamp2str(timestamp){
  let date = new Date(timestamp * 1000);
  return date.toLocaleString().replace(", ", "<br>");
  l
}

function b64enc(text) {
	return window.btoa(unescape(encodeURIComponent(text)));
}

function b64dec(text) {
	return decodeURIComponent(escape(window.atob(text)));
}