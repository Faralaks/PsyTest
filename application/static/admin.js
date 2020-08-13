let psyList;
let lastKey ;

function getPsyList() {
    jq.post("/admin").done( function (psys) {
        psyList = psys;
        showPsy();
    });
    

}

function showPsy(key) {
    let psyTable = jq("#psyTable");
    jq('td').remove();

    if (key) {
        if (key===lastKey) { reverse *= -1; }
        else { reverse = 1; lastKey = key; }

        psyList.sort(function (a, b) {
  if (a[key] > b[key]) {
    return reverse;
  }
  if (a[key] < b[key]) {
    return -1*reverse;
  }
  // a должно быть равным b
  return 0;
});
    }

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
            .append(jq(`<td><a class="btn btn-primary" href="/psy_info/${psyList[i].login}">Подробнее</a></td>`));
        psyTable.append(trPsy);
    }

}