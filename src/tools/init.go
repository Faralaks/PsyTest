package tools

import (
	"crypto/aes"
	"crypto/cipher"
	"log"
	"os"
)

func init() {
	var err error
	go ReadFeedBack()
	FeedBack = make(chan interface{})
	FeedBack <- "FeedBack is ready!"

	CurPath, err = os.Getwd()
	if err != nil {
		VPrint("PANIC!!!", err)
		panic(err)
	}
	FeedBack <- "CurPath is " + CurPath

	c, err := aes.NewCipher(pasSecret)
	if err != nil {
		log.Println(err)
		panic(err)
	}
	gcm, err = cipher.NewGCM(c)
	if err != nil {
		log.Println(err)
		panic(err)
	}
	FeedBack <- "Crypto is ready!"

}
