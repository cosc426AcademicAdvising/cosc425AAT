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

// getFourYearPoliciesbyMajor
app.get("/FourYear/Policy/:major", (req, res) => {
    var maj = req.params.major;
    collection.find({"major": maj}).project({'policies': 1, _id: 0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getFourYearbyMajor
app.get("/FourYear/:major", (req, res) => {
    var maj = req.params.major;
    collection.findOne({"major": maj},
    (error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.listen(5002, () =>{
    mongo.connect(conn_url, {useUnifiedTopology: true},
        (error, client) => {
            if(error){
                return response.status(500).send(error);
            }
            database = client.db(dbname);
            collection = database.collection("FourYear");
            console.log("Connected to `" + dbname + "`!");
        });
});