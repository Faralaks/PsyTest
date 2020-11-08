package db

import (
	"context"
	"fmt"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"log"
)

const DbName = "psytest"
const UsersColName = "users"
const TokensColName = "tokens"

var Client *mongo.Client
var TokensCol *mongo.Collection
var UsersCol *mongo.Collection

func init() {
	// Create client
	client, err := mongo.NewClient(options.Client().ApplyURI("mongodb://127.0.0.1:27017"))
	if err != nil {
		log.Fatal(err)
	}

	// Create connect
	err = client.Connect(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB!")
	Client = client
	TokensCol = Client.Database(DbName).Collection(TokensColName)
	UsersCol = Client.Database(DbName).Collection(UsersColName)

}
