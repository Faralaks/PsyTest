package hendlers

import (
	"html/template"
	"net/http"
	. "tools"
)

func Index(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	VPrint(CurPath)
	main := CurPath + "/templates/index.html"
	base := CurPath + "/templates/base.html"

	tmpl, err := template.ParseFiles(main, base)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	err = tmpl.ExecuteTemplate(w, "index", nil)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

}

func AdminPage(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	main := CurPath + "/templates/admin.html"
	stats := CurPath + "/templates/stats.html"
	base := CurPath + "/templates/base.html"

	tmpl, err := template.ParseFiles(main, base, stats)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	err = tmpl.ExecuteTemplate(w, "admin", nil)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

}

func PsyPage(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	main := CurPath + "/templates/psy.html"
	stats := CurPath + "/templates/stats.html"
	base := CurPath + "/templates/base.html"

	tmpl, err := template.ParseFiles(main, base, stats)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	err = tmpl.ExecuteTemplate(w, "psy", nil)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

}
