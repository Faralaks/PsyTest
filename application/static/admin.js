let psyList, gradeList;
let lastKey;
let curPsy, curGrade;
let preGeneratedPas;
let gradeCounters = {};
let fullCounter;
let needToReload = false;





function setToDefault() {
    jq("#psyFormLogin").val(curPsy.login);
    jq("#psyFormPas").val(curPsy.pas);
    jq("#psyFormIdent").val(curPsy.ident);
    jq("#psyFormCount").val(curPsy.count);
    jq("#psyFormCheckDel").prop("checked", curPsy.pre_del);
    jq("input").prop("checked", false);
    curPsy.tests.forEach(function (testNumber) {
        jq("#test"+testNumber).prop("checked", true)

    })
}

function saveCurPsy() {
    curPsy.login = jq("#psyFormLogin").val();
    curPsy.pas = jq("#psyFormPas").val();
    curPsy.ident = jq("#psyFormIdent").val();
    curPsy.count = jq("#psyFormCount").val();
    curPsy.pre_del = jq("#psyFormCheckDel").prop("checked");
    curPsy.tests = [];
    jq('.testCheckbox:checked').each(function() { curPsy.tests.push(this.value); });
}



function validateFormData(login, pas, ident, count) {
    if (+validateText(login || jq("#psyFormLogin")) + validatePas(pas || jq("#psyFormPas")) + validateText(ident  || jq("#psyFormIdent")) + validateNum(count  || jq("#psyFormCount")) === 4) {
        jq("#psyFormBtnSave").prop("disabled", false);
    }
    else {
        jq("#psyFormBtnSave").prop("disabled", true);
    }

}


function validateText(elem){
    if(elem.val().match(/[^a-zA-Z0-9]/g) || !elem.val().length) {
        elem.toggleClass("is-invalid", true);
        jq(`#${elem.attr("id")}Msg`).text("Недопустимое значение");
        return false;
    }
    elem.toggleClass("is-invalid", false);
    return true;

}
function validatePas(elem){
    if(elem.val().match(/[^a-zA-Z0-9!"#$%&'()*,./:;=?@_`{|}~]/g) || elem.val().length < 8) {
        elem.toggleClass("is-invalid", true);
        jq(`#${elem.attr("id")}Msg`).text("Недопустимый пароль. Он должен содержать не меннее 8 символов");
        return false;
    }
    elem.toggleClass("is-invalid", false);
    return true;

}



function validateNum(elem){
    if(elem.val().length && +elem.val() > 0) {
        elem.toggleClass("is-invalid", false);
        return true;

    }
    elem.toggleClass("is-invalid", true);
    jq(`#${elem.attr("id")}Msg`).text("Неверное значение");
    return false;


}



function showStats(stats) {
    jq("#loadingIcon").show();
    jq('#stat_psy_count').text(stats.psy_count);
    jq('#stat_whole').text(stats.whole);
    jq('#stat_not_yet').text(stats.not_yet);
    jq('#stat_clear').text(stats.clear);
    jq('#stat_danger').text(stats.danger);
    if (stats.msg)  {
        jq('#stat_msg').text(stats.msg);
        jq('#statsLinesMsg').toggleClass('d-flex', true)
    }
    else {
        jq('#statsLinesMsg').toggleClass('d-flex', false)
    }
    jq("#loadingIcon").hide();

}

function showPsy(key) {
    let psyTable = jq("#psyTable");
    jq('td').remove();

    if (key) {
        if (key === lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }

        psyList.sort(function (a, b) {
            if (a[key] > b[key]) { return reverse; }
            if (a[key] < b[key]) { return -1*reverse; }
            return 0;
        });
    }

    fullCounter = { psy_count: psyList.length, whole: 0, not_yet: 0, clear: 0, danger: 0, msg: 0 };
    let grades, grade;

    for (let i = 0; i < psyList.length; i++) {
        let gradeCounter = { whole: 0, not_yet: 0, clear: 0, danger: 0, msg: 0 };
        grades = psyList[i].grades;

        for (let name in grades) {
            if (!grades.hasOwnProperty(name)) continue;
            grade = grades[name];
            gradeCounter.whole += grade.whole || 0;
            gradeCounter.not_yet += grade.not_yet || 0;
            gradeCounter.clear += grade.clear || 0;
            gradeCounter.danger += grade.danger || 0;
            gradeCounter.msg += grade.msg || 0;
        }
        gradeCounters[psyList[i].login] = gradeCounter;

        let ownStats = `
            <span class="badge badge-light badge-pill" title="Количество испытуемых">${ gradeCounter.whole }</span>
            <span class="badge badge-secondary badge-pill" title="Еще не протестировано">${ gradeCounter.not_yet }</span>
            <span class="badge badge-success badge-pill" title="Вне групп риска">${ gradeCounter.clear }</span>
            <span class="badge badge-danger badge-pill" title="В группах риска">${ gradeCounter.danger }</span>`;
        if (gradeCounter.msg) {
            ownStats += `<span class="badge badge-warning badge-pill" title="Сообщения об удалении">${gradeCounter.msg}</span>`
        }
        let trPsy = jq("<tr></tr>")
            .append(jq(`<td>${psyList[i].ident}</td>`))
            .append(jq(`<td>${psyList[i].login}</td>`))
            .append(jq(`<td>${psyList[i].pas}</td>`))
            .append(jq(`<td>${psyList[i].count}</td>`))
            .append(jq(`<td>${ownStats}</td>`))
            .append(jq(`<td>${psyList[i].tests}</td>`))
            .append(jq(`<td>${ stamp2str(psyList[i].create_date) }</td>`))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showPsyInfo(${i})" value="Подробнее"></td>`));
        if (psyList[i].pre_del) trPsy.append(jq(`<td><i class="fa fa-trash" aria-hidden="true" title="Будет удален менее чем через ${Math.ceil((psyList[i].pre_del - (Date.now() / 1000 | 0))/3600)} ч."></i></td>`));

        psyTable.append(trPsy);

        fullCounter.whole += gradeCounter.whole;
        fullCounter.not_yet += gradeCounter.not_yet;
        fullCounter.clear += gradeCounter.clear;
        fullCounter.danger += gradeCounter.danger;
        fullCounter.msg += gradeCounter.msg;

    }
    showStats(fullCounter);


}


function getPsyList(reloadTable= false) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_psy_list").done(function (response) {
        showMsg(response.msg, response.kind,function () {
            psyList = response.psyList;
            if (reloadTable) showPsy()
        });
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}



function addNewPsy() {
    jq.ajaxSetup({timeout:3000});
    jq.post("/api/add_psy", jq("#addPsyForm").serialize()).done(function (response) {
        showMsg(response.msg, response.kind,function () { clearPsyForm(); getPsyList(true); }, response.field);
    }).fail(function () {
        showMsg("Превышено время ожидания или произошла ошибка на стороне сервера! Операция не выполнена");
    })
}


function editPsy() {
    let addPsyFormData = jq('#addPsyForm').serializeArray();
    addPsyFormData.push({name: 'curLogin', value: curPsy.login});
    jq.ajaxSetup({timeout:3000});
    jq.post("/api/edit_psy",  addPsyFormData).done(function (response) {
        showMsg(response.msg, response.kind,function () { saveCurPsy(); needToReload = true; }, response.field);
    }).fail(function () {
        showMsg("Превышено время ожидания или произошла ошибка на стороне сервера! Операция не выполнена");
    })
}



function showGrades(key) {
    let gradeTable = jq("#gradeTable");
    jq('#gradeTable td').remove();
    if (key) {
        if (key===lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }
        if (key === "name") {
            if (reverse < 0) gradeList = gradeList.sort().reverse();
            else gradeList = gradeList.sort();
        }
        else {
            gradeList.sort(function (a, b) {
                if ((a[1][key] || 0) > (b[1][key] || 0)) {
                    return reverse;
                }
                if ((a[1][key] || 0) < (b[1][key] || 0)) {
                    return -1 * reverse;
                }
                return 0;
            });
        }
    }

    let gradeCounter = { whole: 0, not_yet: 0, clear: 0, danger: 0, msg: 0 };

    for (let i = 0; i < gradeList.length; i++) {
        let grade = gradeList[i][1];
        gradeCounter.whole += grade.whole || 0;
        gradeCounter.not_yet += grade.not_yet || 0;
        gradeCounter.clear += grade.clear || 0;
        gradeCounter.danger += grade.danger || 0;
        gradeCounter.msg += grade.msg || 0;

        let trGrade = jq("<tr></tr>").append(jq(`<td>${atob(gradeList[i][0])}</td>`))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-Light badge-pill">${grade.whole || 0}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-secondary badge-pill">${grade.not_yet || 0}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-success badge-pill">${grade.clear || 0}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-danger badge-pill">${grade.danger || 0}</span>`)))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showGradePage()" value="Просмотреть"></td>`));
        if (grade.msg) {
            trGrade.append(`<td><span class="btn btn-warning my-2 my-sm-0" title="В этом классе есть запросы на удаление результата">
                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp;${grade.msg}</span></td>`);
        }
        gradeTable.append(trGrade);
    }
    showStats(gradeCounter);
    gradeCounters[curPsy.login] = gradeCounter;
}



function getGradeList(reloadTable = false) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_grade_list", { psyLogin: curPsy.login}).done(function (response) {
        showMsg(response.msg, response.kind,function () {
            gradeList = response.gradeList;
            if (reloadTable) showGrades()
        });
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err")


    });
}



function getTesteeList(reloadTable= false) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_testee_list", {psyLogin: curPsy.login}).done(function (response) {
        console.log(response)
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}





function clearPsyForm() {
    jq("#psyFormLogin").val("");
    jq("#psyFormPas").val(generatePas(12));
    jq("#psyFormIdent").val("");
    jq("#psyFormCount").val("");
    jq(".testCheckbox:checked").prop("checked", false)
}


function showPsyInfo(psyIdx) {
    curPsy = psyList[psyIdx];
    setToDefault();

    jq("#psyTablePlace").hide();
    jq("#statsLinesPsyCount").removeClass("d-flex").hide();

    jq("#gradeTablePlace").show();
    jq("#psyFormBtnDef").show();
    jq("#psyFormPlaceDel").show();
    jq("#barBtnBack").click(function () { showAdminMainPage() }).show();

    jq("#psyFormTitle").text("Редактировать Психолога");
    jq("#statsCardTitle").text(`${curPsy.login} | Статистика`);
    jq("#psyFormBtnSave").attr("onclick", "editPsy()").val("Сохранить");
    jq("#statsCardBtnRefresh").attr("onclick", "getGradeList(true)");

    jq("input").toggleClass("is-invalid", false);
    jq("#psyFormBtnSave").prop("disabled", true);
    showStats(gradeCounters[curPsy.login]);
    getGradeList(true);

}


function showAdminMainPage() {
    clearPsyForm();
    curPsy = undefined;

    if (needToReload) getPsyList(true);

    jq("#psyTablePlace").show();

    jq("#statsLinesPsyCount").addClass("d-flex").show();

    jq("#gradeTablePlace").hide();
    jq("#psyFormBtnDef").hide();
    jq("#psyFormPlaceDel").hide();
    jq("#barBtnBack").hide();

    jq("#psyFormTitle").text("Добавить психолога");
    jq("#statsCardTitle").text(`Полная статистика`);
    jq("#psyFormBtnSave").attr("onclick", "addNewPsy()").val("Добавить психолога");
    jq("#psyFormPas").val(preGeneratedPas);
    jq("#statsCardBtnRefresh").attr("onclick", "getPsyList(true)");

    jq("input").toggleClass("is-invalid", false);
    jq("#psyFormBtnSave").prop("disabled", true);
    showStats(fullCounter);


}


function showGradePage(gradeIdx) {
    curGrade = gradeList[gradeIdx];
    jq("#add_psy_card").slideToggle(true)


    jq("#gradeTablePlace").show();
    jq("#psyFormBtnDef").show();
    jq("#psyFormPlaceDel").show();
    jq("#barBtnBack").click(function () { showAdminMainPage() }).show();

    jq("#psyFormTitle").text("Редактировать Психолога");
    jq("#statsCardTitle").text(`${curPsy.login} | Статистика`);
    jq("#psyFormBtnSave").attr("onclick", "editPsy()").val("Сохранить");
    jq("#statsCardBtnRefresh").attr("onclick", "getGradeList(true)");

    jq("input").toggleClass("is-invalid", false);
    jq("#psyFormBtnSave").prop("disabled", true);
    showStats(gradeCounters[curPsy.login]);
    getGradeList(true);

}


jq("#psyTablePlace").ready(function () {
    getPsyList(true);


});

