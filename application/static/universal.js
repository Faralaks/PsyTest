let fieldNamesDecode = {
    Login: "Логин",
    Ident: "Идентификатор"
};



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