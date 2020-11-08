package tools

import "crypto/cipher"

var pasSecret = []byte("passphrasewhichneedstobe32bytes!")
var gcm cipher.AEAD

var accessSecret = []byte("access")
var refreshSecret = []byte("refresh")
