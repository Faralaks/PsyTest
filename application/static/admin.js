let psyList, gradeList, testeeList;
let curPsy, curGrade;
let gradeCounters = {};
let fullCounter;
let needToReload = false;


function download() { alert("Эта функция пока недоступна") }


function setToDefault() {
    jq("#psyFormBtnSave").prop("disabled", true);
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



function validateFormData(login=jq("#psyFormLogin"), pas=jq("#psyFormPas"), ident=jq("#psyFormIdent"), count=jq("#psyFormCount")) {
    jq("#psyFormBtnSave").prop("disabled", !(+validateText(login) + validatePas(pas) + validateText(ident) + validateNum(count) === 4));
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
    if(elem.val().match(/[^a-zA-Z0-9!"#$%&'()*,./:;=?@_`{|}~]/g) || elem.val().length < 9) {
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


function showPsy(key) {
    let psyTable = jq("#psyTable");
    jq('td').remove();
    sort(psyList, key);

    fullCounter = { psyCount: psyList.length, whole: 0, not_yet: 0, clear: 0, danger: 0, msg: 0 };
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
            .append(jq(`<td>${psyList[i].login}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${psyList[i].pas}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${psyList[i].count}</td>`))
            .append(jq(`<td>${ownStats}</td>`))
            .append(jq(`<td>${psyList[i].tests}</td>`))
            .append(jq(`<td>${ stamp2str(psyList[i].create_date) }</td>`))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showPsyInfoPage(${i})" value="Подробнее"></td>`));
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


function getPsyList(reloadTable= true) {
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



function acceptDel(testeeLogin, btn) {
    jq.ajaxSetup({timeout:3000});
    jq.post("/api/accept_del", {testeeLogin: testeeLogin}).done(function (response) {
        showMsg(response.msg, response.kind, function () {
            jq(btn).hide();
            gradeCounters[curPsy.login].msg -= 1;
            jq("#stat_msg").text(gradeCounters[curPsy.login].msg);
            if (gradeCounters[curPsy.login].msg === 0) jq("#statsLinesMsg").toggleClass("d-flex", false).hide();
        });
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
    sort(gradeList, key);

    let gradeCounter = { gradeCount: gradeList.length, whole: 0, not_yet: 0, clear: 0, danger: 0, msg: 0 };

    for (let i = 0; i < gradeList.length; i++) {
        let grade = gradeList[i];
        gradeCounter.whole += grade.whole;
        gradeCounter.not_yet += grade.not_yet;
        gradeCounter.clear += grade.clear;
        gradeCounter.danger += grade.danger;
        gradeCounter.msg += grade.msg;

        let trGrade = jq("<tr></tr>").append(jq(`<td>${grade.dec_name}</td>`))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-Light badge-pill">${grade.whole}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-secondary badge-pill">${grade.not_yet}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-success badge-pill">${grade.clear}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-danger badge-pill">${grade.danger}</span>`)))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showGradePage(${i})" value="Просмотреть"></td>`));
        if (grade.msg) {
            trGrade.append(`<td><span class="btn btn-warning my-2 my-sm-0" title="В этом классе есть запросы на удаление результата">
                <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>&nbsp;${grade.msg}</span></td>`);
        }
        gradeTable.append(trGrade);
    }
    showStats(gradeCounter);
    gradeCounters[curPsy.login] = gradeCounter;
}



function getGradeList(reloadTable = true) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_grade_list", { psyLogin: curPsy.login}).done(function (response) {
        showMsg(response.msg, response.kind,function () {
            gradeList = [];
            for (let name in response.gradeList) {
                if (!response.gradeList.hasOwnProperty(name)) continue;
                gradeList.push({
                    name: name,
                    dec_name: atob(name),
                    whole: response.gradeList[name].whole || 0,
                    not_yet: response.gradeList[name].not_yet || 0,
                    clear: response.gradeList[name].clear || 0,
                    danger: response.gradeList[name].danger || 0,
                    msg: response.gradeList[name].msg || 0})
            }
            if (reloadTable) showGrades()
        });
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err")


    });
}




function showTestees(key) {
    let testeeTable = jq("#testeeTable");
    jq('#testeeTable td').remove();
    sort(testeeList, key);

    let gradeCounter = { whole: testeeList.length, not_yet: 0, clear: 0, danger: 0, msg: 0 };

    for (let i = 0; i < testeeList.length; i++) {
        let testee = testeeList[i];
        gradeCounter[resultDecode[testee.result][0]] += 1;

        let trTestee = jq("<tr></tr>")
            .append(jq(`<td><span class="badge badge-${resultDecode[testee.result][1]} badge-pill">${testee.result}</span></td>`))
            .append(jq(`<td>${testee.login}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${testee.pas}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${stamp2str(testee.create_date)}</td>`));

        if (testee.msg) {
            gradeCounter.msg += 1;
            trTestee.append(`<td>
            <div class="btn-group" id="delBtn${i}" >
                    <span data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" class="btn btn-warning my-2 my-sm-0" title="Нажмите, для просмотра сообщения об удалении">
                            <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
                    </span>
                    <div class="dropdown-menu">
                        <div class="card border-0 shadow" id="show_msg_card">
                            <div class="card-body">
                                <h5 class="card-title">Причина удаления</h5>
                                <p>${b64dec(testee.msg)}</p>
                                <input type="button" class="btn btn-primary mr-5 ml-5" value="Подтвердить удаление" onclick="acceptDel('${testee.login}', delBtn${i})">
                        </div>
                    </div>
                </div>
            </div>
        </td>`);
        }
        testeeTable.append(trTestee);
    }
    showStats(gradeCounter);
    gradeCounters[curPsy.login] = gradeCounter;

}


function getTesteeList(reloadTable= true) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_testee_list", {psyLogin: curPsy.login, grade: curGrade.dec_name}).done(function (response) {
        testeeList = response.testeeList
        if (reloadTable) showTestees()
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}



function clearPsyForm() {
    jq("#psyFormBtnSave").prop("disabled", true);
    jq("#psyFormLogin").val("");
    jq("#psyFormPas").val(generatePas(12));
    jq("#psyFormIdent").val("");
    jq("#psyFormCount").val("");
    jq(".testCheckbox:checked").prop("checked", false)
}


function showPsyInfoPage(psyIdx) {
    if (curGrade) { curGrade = undefined; jq("#add_psy_card").slideToggle(); jq("#testeeTablePlace").hide(); }
    else curPsy = psyList[psyIdx];

    setToDefault();

    jq("#psyTablePlace").hide();
    jq("#statsLinesPsyCount").removeClass("d-flex").hide();

    jq("#gradeTablePlace").show();
    jq("#psyFormBtnDef").show();
    jq("#psyFormPlaceDel").show();
    jq("#barBtnBack").off("click").click(showAdminMainPage).show();

    jq("#psyFormTitle").text("Редактировать Психолога");
    jq("#statsCardTitle").text(`${curPsy.login} | Статистика`);
    jq("#psyFormBtnSave").off("click").click(function () { rareCall(editPsy) }).val("Сохранить");
    jq("#statsCardBtnRefresh").off("click").click(function () { rareCall(getGradeList) });

    jq("input").toggleClass("is-invalid", false);
    jq("#psyFormBtnSave").prop("disabled", true);
    showStats(gradeCounters[curPsy.login]);
    getGradeList();

}


function showAdminMainPage() {
    clearPsyForm();
    curPsy = undefined;

    jq("#psyTablePlace").show();
    jq("#statsLinesPsyCount").addClass("d-flex").show();

    jq("#gradeTablePlace").hide();
    jq("#psyFormBtnDef").hide();
    jq("#psyFormPlaceDel").hide();
    jq("#barBtnBack").hide();

    jq("#psyFormTitle").text("Добавить психолога");
    jq("#statsCardTitle").text(`Полная статистика`);

    jq("#psyFormBtnSave").off("click").click(function () { rareCall(addNewPsy) }).val("Добавить психолога");
    jq("#statsCardBtnRefresh").off("click").click(function () { rareCall(getPsyList) });

    jq("input").toggleClass("is-invalid", false);
    jq("#psyFormBtnSave").prop("disabled", true);

    showStats(fullCounter);
    if (needToReload) { getPsyList(); needToReload = false}

}


function showGradePage(gradeIdx) {
    curGrade = gradeList[gradeIdx];
    jq("#add_psy_card").slideToggle();

    jq("#gradeTablePlace").hide();

    jq("#testeeTablePlace").show();
        jq("#barBtnBack").off("click").click(showPsyInfoPage);

    jq("#gradeName").text(curGrade.dec_name);

    jq("#statsCardTitle").text(`${curGrade.dec_name} | Статистика`);
    jq("#statsCardBtnRefresh").off("click").click(function () { rareCall(getTesteeList) });

    showStats(curGrade);
    getTesteeList();
    needToReload = true;

}


jq("#psyTablePlace").ready(getPsyList);
jq("#psyFormBtnSave").ready(function () { jq("#psyFormBtnSave").click(addNewPsy) });
jq("#statsCardBtnRefresh").ready(function () { jq("#statsCardBtnRefresh").click(function () { rareCall(getPsyList) }) });
jq("#statsCardBtnDownload").ready(function () { jq("#statsCardBtnDownload").click(function () { rareCall(download) }) });




