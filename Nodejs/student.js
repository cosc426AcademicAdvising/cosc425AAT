const express = require("express");
const bodyparser = require("body-parser");
const mongo = require("mongodb").MongoClient;
const obj = require("mongodb").ObjectID;
const { response } = require("express");
const conn_url = "mongodb+srv://COSC425AAT:ucciEcY4ItzL6BRN@cluster0.qmhln.mongodb.net/test?authSource=admin&replicaSet=atlas-udg01y-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true";
const dbname = "COSC425AAT";

var app = express();
app.use(bodyparser.json());
app.use(bodyparser.urlencoded({extended: true}));
var database, collection;

// getStudentbyID
app.get("/Student/:id", (req, res) => {
    var sid = parseInt(req.params.id);
    collection.findOne({"s_id": sid},
    (error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.listen(5000, () =>{
    mongo.connect(conn_url, {useUnifiedTopology: true},
        (error, client) => {
            if(error){
                return response.status(500).send(error);
            }
            database = client.db(dbname);
            collection = database.collection("Student");
            console.log("Connected to `" + dbname + "`!");
        });
});