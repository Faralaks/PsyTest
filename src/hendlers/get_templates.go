package hendlers

import (
	"html/template"
	"net/http"
)

func Index(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	main := "templates/index.html"
	base := "templates/base.html"

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
	main := "templates/admin.html"
	stats := "templates/stats.html"
	base := "templates/base.html"

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
	main := "templates/psy.html"
	stats := "templates/stats.html"
	base := "templates/base.html"

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
