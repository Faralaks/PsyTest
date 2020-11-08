package hendlers

import (
	"net/http"
	. "tools"
)

func AuthMiddleware(next http.Handler, allowList []string) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		//println("~~~~~~~~~~~ AuthMiddleware")
		cookieAt, err := r.Cookie("AccessToken")
		if err != nil || len(cookieAt.Value) == 0 {
			if cookieRt, err := r.Cookie("RefreshToken"); err == nil && len(cookieRt.Value) != 0 {
				//println("------ before RefreshMiddleware")
				RefreshMiddleware(cookieRt, w, r, next)
				return
			}
			JsonMsg{Kind: ReloginKind, Msg: "Не были получены необходимые ключи | " + err.Error()}.SendMsg(w)
			return
		}
		//println("======= after RefreshMiddleware")

		at := cookieAt.Value
		claims, err := ExtractAt(at)
		if err != nil {
			JsonMsg{Kind: FatalKind, Msg: "Недействительный ключ авторизации | " + err.Error()}.SendMsg(w)
			return
		}
		//println(">>>>>>"+claims["owner"].(string))
		for _, status := range allowList {
			if status == claims["status"].(string) {
				r.Header.Set("status", claims["status"].(string))
				r.Header.Set("owner", claims["owner"].(string))

				next.ServeHTTP(w, r)
				return
			}
		}

		JsonMsg{Kind: ReloginKind, Msg: "Отказано в доступе"}.SendMsg(w)

	})
}
