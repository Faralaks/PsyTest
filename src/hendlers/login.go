package hendlers

import (
	"context"
	"encoding/json"
	"go.mongodb.org/mongo-driver/bson"
	"net/http"
	"time"
	. "tools"
)

type LoginDataResponse struct {
	Status       string `json:"status"`
	AccessToken  string `json:"accessToken"`
	RefreshToken string `json:"refreshToken"`
}

func Login(w http.ResponseWriter, r *http.Request) {
	login := NewB64LowString(TrimStr(r.FormValue("login"), 40))
	pas := Encrypt(TrimStr(r.FormValue("password"), 50))

	var user User
	ctx, _ := context.WithTimeout(context.Background(), 3*time.Second)
	err := UsersCol.FindOne(ctx, bson.M{"login": login, "pas": pas, "deleteDate": bson.D{{"$exists", false}}}).Decode(&user)
	if err != nil {
		DeleteCookie(w)
		JsonMsg{Kind: BadAuthKind}.SendMsg(w)
		return
	}

	signedAt, signedRt, err := CreateTokens(user.Uid.Hex(), user.Status)
	if err != nil {
		JsonMsg{Kind: FatalKind, Msg: "Не удалось создать токены | " + err.Error()}.SendMsg(w)
		return
	}
	http.SetCookie(w, &http.Cookie{Name: "AccessToken", Value: signedAt, HttpOnly: true, Expires: time.Now().UTC().Add(Config.ATLifeTime)})
	http.SetCookie(w, &http.Cookie{Name: "RefreshToken", Value: signedRt, HttpOnly: true, Expires: time.Now().UTC().Add(Config.RTLifeTime)})

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(LoginDataResponse{user.Status, signedAt, signedRt})

}
