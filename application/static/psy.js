let curPsy, curGrade;
let gradeList, testeeList;
let psyCounter, gradeCounter;

function download() { alert("Эта функция пока недоступна") }

function validateFormData() {
    jq("#addFormBtnAdd").prop("disabled", !(+validateText(jq("#addFormName")) + validateNum(jq("#addFormCount")) === 2));
}

function validateText(elem){
    if(elem.val().match(/[^a-zA-Zа-яА-Я0-9«»“”"„ ]/g) || !elem.val().length) {
        elem.toggleClass("is-invalid", true);
        jq(`#${elem.attr("id")}Msg`).text("Недопустимое значение");
        return false;
    }
    elem.toggleClass("is-invalid", false);
    return true;

}
function validateNum(elem){
    if(elem.val().length && +elem.val() > 0 && +elem.val() <= curPsy.count) {
        elem.toggleClass("is-invalid", false);
        return true;
    }
    elem.toggleClass("is-invalid", true);
    jq(`#${elem.attr("id")}Msg`).text("Недопустимое значение");
    return false;


}

function renderGradeList(list) {
    gradeList = [];
    for (let name in list) {
        if (!list.hasOwnProperty(name)) continue;
        gradeList.push({name: name,
        dec_name: atob(name),
        whole: list[name].whole || 0,
        not_yet: list[name].not_yet || 0,
        clear: list[name].clear || 0,
        danger: list[name].danger || 0,
        msg: list[name].msg || 0})
    }
}

function clearTesteeForm() {
    jq("#addFormBtnAdd").prop("disabled", true);
    alert(curGrade)
    if (!curGrade) jq("#addFormName").prop("readonly", false).val("");
    else jq("#addFormName").prop("readonly", true).val(curGrade.dec_name);
    jq("#addFormCount").val("");
    jq("input").toggleClass("is-invalid", false);
}


function showGrades(key) {
    let gradeTable = jq("#gradeTable");
    jq('#gradeTable td').remove();
    sort(gradeList, key);

    psyCounter = { gradeCount: gradeList.length, whole: 0, not_yet: 0, clear: 0, danger: 0};

    for (let i = 0; i < gradeList.length; i++) {
        let grade = gradeList[i];
        psyCounter.whole += grade.whole;
        psyCounter.not_yet += grade.not_yet;
        psyCounter.clear += grade.clear;
        psyCounter.danger += grade.danger;

        let trGrade = jq("<tr></tr>").append(jq(`<td>${grade.dec_name}</td>`))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-Light badge-pill">${grade.whole}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-secondary badge-pill">${grade.not_yet}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-success badge-pill">${grade.clear}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-danger badge-pill">${grade.danger}</span>`)))
            .append(jq(`<td><input type="button" class="btn btn-success" onclick="showGradePage(${i})" value="Просмотреть"></td>`));
        gradeTable.append(trGrade);
    }
    showStats(psyCounter);
}


function deleteResult(testeeIdx, btn) {
    let testee = testeeList[testeeIdx];
    jq.ajaxSetup({timeout:2000});
    jq.post("/api/del_result", {testeeLogin: testee.login, prevRes: testee.result, reason: jq("#delReasonField").val(), grade: curGrade.dec_name}).done(function (response) {
        showMsg(response.msg, response.kind, function () {
            jq(btn).hide();
            gradeCounter[resultDecode[testee.result][0]] -= 1;
            jq("#stat_"+resultDecode[testee.result][0]).text(gradeCounter[resultDecode[testee.result][0]]);
            gradeCounter.not_yet += 1;
            jq("#stat_not_yet").text(gradeCounter.not_yet);
            testeeList[testeeIdx].result = "Нет результата"
            jq("#resultPlace"+testeeIdx).text(testeeList[testeeIdx].result).toggleClass("badge-"+resultDecode[testee.result][1], false).toggleClass("badge-secondary", true);
        });
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}


function showTestees(key) {
    let testeeTable = jq("#testeeTable");
    jq('#testeeTable td').remove();
    sort(testeeList, key);

    gradeCounter = { whole: testeeList.length, not_yet: 0, clear: 0, danger: 0 };

    for (let i = 0; i < testeeList.length; i++) {
        let testee = testeeList[i];
        gradeCounter[resultDecode[testee.result][0]] += 1;
        let trTestee = jq("<tr></tr>")
            .append(jq(`<td><span id="resultPlace${i}" class="badge badge-${resultDecode[testee.result][1]} badge-pill">${testee.result}</span></td>`))
            .append(jq(`<td>${testee.login}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${testee.pas}</td>`).click(function () { copyText(this) }))
            .append(jq(`<td>${stamp2str(testee.create_date)}</td>`));

        if (testee.result !== "Нет результата") {
            trTestee.append(`<td>
            <div class="btn-group" id="delBtn${i}" >
                    <span data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" class="btn btn-outline-danger my-2 my-sm-0" title="Нажмите, чтобы удалить результат">
                            <i class="fa fa-trash" aria-hidden="true"></i>
                    </span>
                    <div class="dropdown-menu">
                        <div class="card border-0 shadow" id="show_msg_card">
                            <div class="card-body">
                            <h5 class="card-title">Введите причину удаления результата испытуемого ${testee.login} из ${curGrade.dec_name}</h5>
                            <textarea id="delReasonField" style="width: 600px" class="form-control" rows="2" required maxlength="500" aria-describedby="stopLen" name="reason"></textarea>
                            <small id="stopLen" class="form-text text-muted">Не более 500 символов</small>
                            <br>
                            <input type="button" class="btn btn-danger" value="Удалить" onclick="deleteResult('${i}', delBtn${i})">
                        </div>
                    </div>
                </div>
            </div>
        </td>`);
        }
        testeeTable.append(trTestee);
    }
    showStats(gradeCounter);

}


function getTesteeList(reloadTable= true) {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:10000});
    jq.post("/api/get_testee_list", {psyLogin: curPsy.login, grade: curGrade.dec_name}).done(function (response) {
        testeeList = response.testeeList
        if (reloadTable) showTestees()
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}



function getUserData() {
    jq("#loadingIcon").show();
    jq.ajaxSetup({timeout:2000});
    jq.post("/api/get_user_data").done(function (response) {
        curPsy = response.userData;
        setLogin(curPsy.login, gradeList);
        jq("#countPlace").text(curPsy.count);
        jq("#addFormCount").prop("max", curPsy.count);
        renderGradeList(curPsy.grades);
        showGrades()
    }).fail(function () { jq("#loadingIcon").hide(); showMsg('Данные загрузить не удалось', "Err") });
}


function addTestees() {
    jq.ajaxSetup({timeout:3000});
    jq.post("/api/add_testees", jq("#addTesteesForm").serialize()).done(function (response) {
        showMsg(response.msg, response.kind, function () {
            if (!curGrade) { getUserData(); return }
            curPsy.count -= +jq("#addFormCount").val();
            jq("#countPlace").text(curPsy.count);
            jq("#addFormCount").prop("max", curPsy.count);
            clearTesteeForm();
            getTesteeList() });
    }).fail(function () {
        showMsg("Превышено время ожидания или произошла ошибка на стороне сервера! Операция не выполнена");
    })
}



function showGradePage(gradeIdx) {
    curGrade = gradeList[gradeIdx];
    clearTesteeForm();
    jq("#gradeTablePlace").hide();

    jq("#testeeTablePlace").show();
    jq("#barBtnBack").off("click").click(showPsyMainPage).show();

    jq("#gradeName").text(curGrade.dec_name);

    jq("#statsCardTitle").text(`${curGrade.dec_name} | Статистика`);
    jq("#statsCardBtnRefresh").off("click").click(function () { rareCall(getTesteeList) });

    showStats(curGrade);
    getTesteeList();
}


function showPsyMainPage() {
    curGrade = undefined;
    testeeList = undefined;
    gradeCounter = undefined;
    clearTesteeForm();

    jq("#gradeTablePlace").show();

    jq("#testeeTablePlace").hide();
    jq("#barBtnBack").off("click").hide();

    jq("#statsCardTitle").text("Общая статистика");
    jq("#statsCardBtnRefresh").off("click").click(function () { rareCall(getUserData) });

    showStats(psyCounter);
    getUserData();
}





jq("#gradeTablePlace").ready(function () { getUserData() });
jq("#statsCardBtnRefresh").ready(function () { jq("#statsCardBtnRefresh").click(function () { rareCall(getUserData) }) });
jq("#statsCardBtnDownload").ready(function () { jq("#statsCardBtnDownload").click(function () { rareCall(download) }) });
