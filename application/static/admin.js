let psyList;
let lastKey;
let stats;
let curPsy;
let gradeList, gradeStats;

function showMsg(msg, status) {
    status = "msg" + status;
    let msgLine = jq("#msg");
    msgLine.removeClass();
    msgLine.text(msg).addClass(status).fadeIn(1000).delay(5000).fadeOut(1000);
}

function showStats(stats) {
    jq('#stat_psy_count').text(stats.psy_count);
    jq('#stat_whole').text(stats.whole);
    jq('#stat_not_yet').text(stats.not_yet);
    jq('#stat_clear').text(stats.clear);
    jq('#stat_danger').text(stats.danger);
    if (stats.msg)  {
        jq('#stat_msg').text(stats.msg);
        jq('#statsLinesMsg').addClass('d-flex').show()
    }
    else {
        jq('#statsLinesMsg').removeClass('d-flex').hide()
    }

}

function showPsy(key) {
    let psyTable = jq("#psyTable");
    jq('td').remove();

    if (key) {
        if (key===lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }

        psyList.sort(function (a, b) {
        if (a[key] > b[key]) { return reverse; }
        if (a[key] < b[key]) { return -1*reverse; }
        return 0;
        });
    }




    for (let i = 0; i < psyList.length; i++) {
        let ownStats = `
            <span class="badge badge-light badge-pill" title="Количество испытуемых">${ psyList[i].counters.whole}</span>
            <span class="badge badge-secondary badge-pill" title="Еще не протестировано">${ psyList[i].counters.not_yet }</span>
            <span class="badge badge-success badge-pill" title="Вне групп риска">${ psyList[i].counters.clear }</span>
            <span class="badge badge-danger badge-pill" title="В группах риска">${ psyList[i].counters.danger }</span>`;
        if (psyList[i].counters.msg) {
            ownStats += `<span class="badge badge-warning badge-pill" title="Сообщения об удалении">${psyList[i].counters.msg}</span>`
        }
        let trPsy = jq("<tr></tr>")
            .append(jq(`<td>${psyList[i].ident}</td>`))
            .append(jq(`<td>${psyList[i].login}</td>`))
            .append(jq(`<td>${psyList[i].pas}</td>`))
            .append(jq(`<td>${psyList[i].count}</td>`))
            .append(jq(`<td>${ownStats}</td>`))
            .append(jq(`<td>${psyList[i].tests}</td>`))
            .append(jq(`<td>${psyList[i].create_date.replace(' ', '<br>')}</td>`))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showPsyInfo(${i})" value="Подробнее"></td>`));
        if (psyList[i].pre_del) trPsy.append(jq(`<td><i class="fa fa-trash" aria-hidden="true" title="Будет удален менее чем через ${Math.ceil((psyList[i].pre_del - (Date.now() / 1000 | 0))/3600)} ч."></i></td>`));

        psyTable.append(trPsy);

    }

}


function getPsyList() {
    jq.ajaxSetup({timeout:10000});
    jq.post("/admin").done(function (psysAndStats) {
        psyList = psysAndStats.psys;
        stats = psysAndStats.stats;
        showPsy();
        showStats(stats)
    }).fail(function () { showMsg('Данные загрузить не удалось', "Err")

    });
}

function addNewPsy() {
    jq.ajaxSetup({timeout:3000});
    jq.post("/add_psy", jq("#addPsyForm").serialize()).done(function (response) {
        showMsg(response.msg, response.status);
        if (response.status === "Suc") getPsyList();
    }).fail(function () {
        showMsg("Превышено время ожидания или произошла ошибка на стороне сервера, Психолог не добавлен", 'Err')

    })
}



function showGrades(key) {
    let gradeTable = jq("#gradeTable");
    jq('td').remove();

    if (key) {
        if (key===lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }

        psyList.sort(function (a, b) {
        if (a[key] > b[key]) { return reverse; }
        if (a[key] < b[key]) { return -1*reverse; }
        return 0;
        });
    }




    for (let i = 0; i < gradeList.length; i++) {
        let trGrade = jq("<tr></tr>").append(jq(`<td>${atob(gradeList[i][0])}</td>`))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-Light badge-pill">${gradeList[i][1].whole}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-secondary badge-pill">${gradeList[i][1].not_yet}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-secondary badge-pill">${gradeList[i][1].clear}</span>`)))
            .append(jq("<td></td>").append(jq(`<span class="badge badge-danger badge-pill">${gradeList[i][1].danger}</span>`)))
            .append(jq(`<td><input type="button" class="btn btn-primary" onclick="showsyInfo(${i})" value="Просптреть"></td>`));

        gradeTable.append(trGrade);

    }

}




function getGradeList() {
    jq.ajaxSetup({timeout:10000});
    jq.post(`/get_grade_list/${curPsy.login}`).done(function (gradesAndStats) {
        gradeList = gradesAndStats.grades;
        gradeStats = gradesAndStats.stats;
        console.log(gradeList);
        showStats(gradeStats)
        showGrades();
    }).fail(function () { showMsg('Данные загрузить не удалось', "Err")


    });
}


function setToDefault() {
    jq("#psyFormLogin").val(curPsy.login);
    jq("#psyFormPas").val(curPsy.pas);
    jq("#psyFormIdent").val(curPsy.ident);
    jq("#psyFormCount").val(curPsy.count);
    jq("#psyFormCheckDel").prop("checked", curPsy.pre_del);
}

function showPsyInfo(psyIdx) {
    curPsy = psyList[psyIdx];
    setToDefault();


    jq("#psyTablePlace").hide();
    jq("#statsLinesPsyCount").removeClass("d-flex").hide();

    jq("#gradeTablePlace").show();
    jq("#psyFormBtnDef").show();
    jq("#psyFormPlaceDel").show();
    jq("#barBtnBack").show();

    jq("#psyFormTitle").text("Редактировать Психолога");
    jq("#statsCardTitle").text(`${curPsy.login} | Статистика`);
    jq("#psyFormBtnSave").val("Сохранить");

    showStats(curPsy.counters)
    getGradeList();



}
