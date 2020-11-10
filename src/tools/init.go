package tools

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/json"
	"io/ioutil"
	"os"
	"runtime"
	"strings"
)

func init() {
	var err error
	go ReadFeedBack()
	FeedBack = make(chan interface{})
	FeedBack <- "FeedBack is ready!"

	folder := "."
	if runtime.GOOS != "darwin" {
		exec, _ := os.Executable()
		path := strings.Split(exec, "/")
		folder = strings.Join(path[:len(path)-1], "/")
	}

	configFile, err := ioutil.ReadFile(folder + "/config.json")
	if err != nil {
		VPrint("PANIC!!!  Ошибка при открытии конфига", err)
		panic(err)
	}

	err = json.Unmarshal(configFile, &configData)
	if err != nil {
		VPrint("PANIC!!!  Ошибка при декодировании JSON-конфига |" + err.Error())
		panic(err.Error())
	}

	Config.AccessSecret = []byte(configData["accessSecret"])
	Config.RefreshSecret = []byte(configData["refreshSecret"])
	Config.PasSecret = []byte(configData["pasSecret"])
	Config.Port = configData["port"]
	Config.Address = configData["address"]
	Config.CurPath = configData["curPath"]
	FeedBack <- "Config is ready"

	c, err := aes.NewCipher(Config.PasSecret)
	if err != nil {
		VPrint(err.Error())
		panic(err)
	}
	Config.Gcm, err = cipher.NewGCM(c)
	if err != nil {
		VPrint(err.Error())
		panic(err)
	}
	FeedBack <- "Crypto is ready!"

}
