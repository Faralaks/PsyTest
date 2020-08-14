let psyList;
let lastKey;
let stats;


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
    jq('#stat_psy_count').text(stats.psy_count);
    jq('#stat_whole').text(stats.whole);
    jq('#stat_not_yet').text(stats.not_yet);
    jq('#stat_clear').text(stats.clear);
    jq('#stat_danger').text(stats.danger);
    if (stats.msg)  jq('#stat_msg').text(stats.msg);
    else {jq('#stat_msg').parent().remove()}



    for (let i = 0; i < psyList.length; i++) {
        let ownStats = `
            <span class="badge badge-light badge-pill" title="Количество испытуемых">${ psyList[i].counters.whole}</span>
            <span class="badge badge-secondary badge-pill" title="Еще не протестировано">${ psyList[i].counters.not_yet }</span>
            <span class="badge badge-success badge-pill" title="Вне групп риска">${ psyList[i].counters.clear }</span>
            <span class="badge badge-danger badge-pill" title="В группах риска">${ psyList[i].counters.danger }</span>`;
        if (psyList[i].counters.msg) {
            ownStats += `<span class="badge badge-warning badge-pill" title="Сообщения об удалении">${psyList[i].counters.msg}</span>`
        }
        let preDel;
        if (psyList[i].pre_del) { preDel = (psyList[i].pre_del - (Date.now() / 1000 | 0))/3600 | 0}
        else { preDel = '-' }
        let trPsy = jq("<tr></tr>")
            .append(jq(`<td>${psyList[i].ident}</td>`))
            .append(jq(`<td>${psyList[i].login}</td>`))
            .append(jq(`<td>${psyList[i].pas}</td>`))
            .append(jq(`<td>${psyList[i].count}</td>`))
            .append(jq(`<td>${ownStats}</td>`))
            .append(jq(`<td>${psyList[i].tests}</td>`))
            .append(jq(`<td>${psyList[i].create_date.replace(' ', '<br>')}</td>`))
            .append(jq(`<td>${preDel}</td>`))
            .append(jq(`<td><a class="btn btn-primary" href="/psy_info/${psyList[i].login}">Подробнее</a></td>`));
        console.log(psyList[i]);
        psyTable.append(trPsy);
    }

}

function getPsyList() {
    jq.post("/admin").done(function (psysAndStats) {
        psyList = psysAndStats.psys;
        stats = psysAndStats.stats;
        showPsy();
    });
}
