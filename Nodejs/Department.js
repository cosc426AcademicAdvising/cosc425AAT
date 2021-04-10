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

// getDistinctSchools
app.get("/Department/School", (req, res) => {
    collection.distinct("School", function(error, result){
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getMajors
app.get("/Department/Major", (req, res) => {
    collection.find({'Plan Type': 'Major'}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

//getMajorsbySchool
app.get("/Department/Major/:school", (req, res) => {
    var name = req.params.school;
    collection.find({'Plan Type': 'Major', 'School': name}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getMinors
app.get("/Department/Minor", (req, res) => {
    collection.find({'Plan Type': 'Minor'}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

//getMinorsbySchool
app.get("/Department/Minor/:school", (req, res) => {
    var name = req.params.school
    collection.find({'Plan Type': 'Minor', 'School': name}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

app.listen(5001, () =>{
    mongo.connect(conn_url, {useUnifiedTopology: true},
        (error, client) => {
            if(error){
                return response.status(500).send(error);
            }
            database = client.db(dbname);
            collection = database.collection("Department");
            console.log("Connected to `" + dbname + "`!");
        });
});