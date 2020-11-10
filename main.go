package main

import (
	"db"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	p "go.mongodb.org/mongo-driver/bson/primitive"
	"golang.org/x/net/context"
	. "hendlers"
	"net/http"
	"os"
	. "tools"
)

func main() {
	r := mux.NewRouter()

	fs := http.FileServer(http.Dir(Config.CurPath + "/public"))
	r.PathPrefix("/js/").Handler(fs)
	r.Path("/favicon.ico").Handler(fs)

	r.HandleFunc("/", Index).Methods("GET")
	r.HandleFunc("/login", Login).Methods("POST")

	r.HandleFunc("/admin", AdminPage).Methods("GET")
	r.HandleFunc("/psy", PsyPage).Methods("GET")

	r.Handle("/api/get_psy_list", AuthMiddleware(Get_psy_list, AdminAccess)).Methods("GET")
	r.Handle("/api/add_psy", AuthMiddleware(Add_psy, AdminAccess)).Methods("POST")
	r.Handle("/api/accept_del", AuthMiddleware(Accept_del, AdminAccess)).Methods("POST")
	r.Handle("/api/edit_psy", AuthMiddleware(Edit_psy, AdminAndPsyAccess)).Methods("POST")
	r.Handle("/api/get_user_data", AuthMiddleware(Get_user_data, AllAccess)).Methods("GET")
	r.Handle("/api/add_testees", AuthMiddleware(Add_testees, PsyAccess)).Methods("POST")
	r.Handle("/api/get_testee_list", AuthMiddleware(Get_testee_list, AdminAndPsyAccess)).Methods("GET")
	r.Handle("/api/del_result", AuthMiddleware(Del_result, PsyAccess)).Methods("POST")
	r.Handle("/api/edit_user_data", AuthMiddleware(Edit_user_data, AdminAndPsyAccess)).Methods("POST")
	r.Handle("/download", AuthMiddleware(Download, AdminAndPsyAccess)).Methods("GET")

	r.HandleFunc("/remake", remakeDb).Methods("GET")
	r.HandleFunc("/logout", logOut).Methods("GET")
	_ = http.ListenAndServe(Config.Address+":"+Config.Port, handlers.LoggingHandler(os.Stdout, r))
}

var logOut = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	http.SetCookie(w, &http.Cookie{Name: "AccessToken", HttpOnly: true, MaxAge: -1})
	http.SetCookie(w, &http.Cookie{Name: "RefreshToken", HttpOnly: true, MaxAge: -1})
	w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")
	http.Redirect(w, r, "/", 301)

})

var remakeDb = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
	db.UsersCol.DeleteMany(context.TODO(), bson.M{})
	db.TokensCol.DeleteMany(context.TODO(), bson.M{})
	u := User{
		Uid:          p.NewObjectID(),
		Login:        NewB64String("master"),
		Pas:          Encrypt("retsam"),
		Status:       AdminStatus,
		CreatedDate:  CurUtcStamp(),
		Owner:        "Faralaks",
		ModifiedDate: CurUtcStamp(),
	}
	db.UsersCol.InsertOne(context.TODO(), u)

	_ = Psy{
		Uid:          p.NewObjectID(),
		Login:        NewB64LowString("psy"),
		Pas:          Encrypt(""),
		Status:       PsyStatus,
		CreatedDate:  CurUtcStamp(),
		Ident:        NewB64LowString("id"),
		Owner:        "Faralaks",
		Available:    9999,
		Tests:        []string{"1", "2"},
		Grades:       Grades{},
		ModifiedDate: CurUtcStamp(),
	}

	//db.UsersCol.InsertOne(context.TODO(), p)
	//_, _ = fmt.Fprint(w, `<a href="/logout" style="font-size: 5em">BACKBACKBACKBACKBACKBACKBACKBACK</a>`)
	w.Header().Set("Cache-Control", "no-cache, no-store, must-revalidate")
	http.Redirect(w, r, "/", 301)

})
