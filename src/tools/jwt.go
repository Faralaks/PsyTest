package tools

import (
	"context"
	"db"
	"fmt"
	jwt "github.com/dgrijalva/jwt-go"
	p "go.mongodb.org/mongo-driver/bson/primitive"
	"time"
)

type AccessTokenData struct {
	Owner     string    `bson:"owner"`
	Status    string    `bson:"status"`
	CreatedAt time.Time `bson:"createdAt"`
}
type RefreshTokenData struct {
	Uuid      string    `bson:"_id"`
	Owner     string    `bson:"owner"`
	Status    string    `bson:"status"`
	CreatedAt time.Time `bson:"createdAt"`
}

func (rt *RefreshTokenData) Save() error {
	ctx, _ := context.WithTimeout(context.Background(), 5*time.Second)
	_, err := db.TokensCol.InsertOne(ctx, rt)
	if err != nil {
		return err
	}
	return nil
}

func CreateTokens(uid string, status string) (string, string, error) {
	atd := &AccessTokenData{
		Owner:     uid,
		Status:    status,
		CreatedAt: time.Now().UTC(),
	}

	atClaims := jwt.MapClaims{}
	atClaims["authorized"] = true
	atClaims["owner"] = atd.Owner
	atClaims["status"] = atd.Status
	atClaims["exp"] = atd.CreatedAt.Add(time.Hour * 10).Unix()
	at := jwt.NewWithClaims(jwt.SigningMethodHS512, atClaims)
	signedAt, err := at.SignedString(accessSecret)
	if err != nil {
		return "", "", err
	}

	rtd := &RefreshTokenData{
		Uuid:      p.NewObjectID().Hex(),
		Owner:     uid,
		Status:    status,
		CreatedAt: time.Now().UTC(),
	}
	rtClaims := jwt.MapClaims{}
	rtClaims["uuid"] = rtd.Uuid
	rtClaims["owner"] = rtd.Owner
	rtClaims["status"] = rtd.Status
	rtClaims["exp"] = rtd.CreatedAt.Add(time.Hour * 10).Unix()
	rt := jwt.NewWithClaims(jwt.SigningMethodHS512, rtClaims)
	signedRt, err := rt.SignedString(refreshSecret)
	if err != nil {
		return "", "", err
	}
	err = rtd.Save()
	if err != nil {
		return "", "", err
	}

	return signedAt, signedRt, nil
}

func ExtractAt(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return accessSecret, nil
	})
	if err != nil {
		return nil, err
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if ok && token.Valid {
		return claims, nil
	}
	return nil, err
}

func ExtractRt(tokenString string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
		}
		return refreshSecret, nil
	})
	if err != nil {
		return nil, err
	}
	claims, ok := token.Claims.(jwt.MapClaims)
	if ok && token.Valid {
		return claims, nil
	}
	return nil, err
}
