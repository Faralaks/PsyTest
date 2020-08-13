function getPsyList() {
    jq.post("/admin").done( function (psyList) {
        let psyTable = jq("#psyTable");
        for (let i = 0; i < psyList.length; i++) {
            let stats = `
                <span class="badge badge-light badge-pill" title="Количество испытуемых">${ psyList[i].counters.whole}</span>
                <span class="badge badge-secondary badge-pill" title="Еще не протестировано">${ psyList[i].counters.not_yet }</span>
                <span class="badge badge-success badge-pill" title="Вне групп риска">${ psyList[i].counters.clear }</span>
                <span class="badge badge-danger badge-pill" title="В группах риска">${ psyList[i].counters.danger }</span>`;
            if (psyList[i].counters.msg) {
                stats += `<span class="badge badge-warning badge-pill" title="Сообщения об удалении">${psyList[i].counters.msg}</span>`
            }
            let trPsy = jq("<tr></tr>")
                .append(jq(`<td>${psyList[i].ident}</td>`))
                .append(jq(`<td>${psyList[i].login}</td>`))
                .append(jq(`<td>${psyList[i].pas}</td>`))
                .append(jq(`<td>${psyList[i].count}</td>`))
                .append(jq(`<td>${stats}</td>`))
                .append(jq(`<td>${psyList[i].tests}</td>`))
                .append(jq(`<td>${psyList[i].create_date.replace(' ', '<br/>')}</td>`))
                .append(jq(`<td>${psyList[i].deleted?psyList[i].deleted:'-'}</td>`))
                .append(jq(`<a class="btn btn-primary" href="/psy_info/${psyList[i].login}">Подробнее</a>`));
             psyTable.append(trPsy);

        }
    });
    

}

function sortPsy(key) {

}