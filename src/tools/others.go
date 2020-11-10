package tools

import (
	"crypto/cipher"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
)

type configType struct {
	CurPath       string
	Port          string
	Address       string
	Gcm           cipher.AEAD
	PasSecret     []byte
	AccessSecret  []byte
	RefreshSecret []byte
	MongoUrl      string
}

var configData map[string]string
var Config = configType{}

var FeedBack chan interface{}
var feedCounter = 0

func ReadFeedBack() {
	for {
		fmt.Printf("%v\n", <-FeedBack)
	}
}

func VPrint(lines ...interface{}) {
	FeedBack <- fmt.Sprintf("\n======= %v   ¯\\_(ツ)_/¯    =======", feedCounter)
	for i, s := range lines {
		if fmt.Sprintf("%T", s) == "string" {
			FeedBack <- fmt.Sprintf("%v %T\t\"%v\" l: %v", i, s, s, len(s.(string)))
		} else {
			FeedBack <- fmt.Sprintf("%v %T\t%v", i, s, s)
		}
	}
	FeedBack <- "=======   ~~~~~~~~~~~~    ======="
	feedCounter++

}

const FatalKind = "Fatal"
const ReloginKind = "Relogin"
const BadAuthKind = "BadAuth"
const SucKind = "Suc"
const BadUpdateKind = "BadUpdate"
const DuplicateKeyKind = "DuplicatedField"

type JsonMsg struct {
	Kind  string `json:"kind,omitempty"`
	Msg   string `json:"msg,omitempty"`
	Field string `json:"field,omitempty"`
}

func (jm JsonMsg) SendMsg(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(jm)
	if jm.Kind != SucKind {
		log.Printf("ErrKind: %v, Msg: %v, Field: %v", jm.Kind, jm.Msg, jm.Field)
	}
}

func Contains(elem string, list []string) bool {
	for _, e := range list {
		if elem == e {
			return true
		}
	}
	return false
}

func TrimStr(str string, l int) string {
	str = strings.TrimSpace(str)
	runes := []rune(str)
	if len(runes) > l {
		str = string(runes[:l])
	}
	return str
}

func GeneratePas() string {
	return "pas"
}
