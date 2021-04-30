const router = require("express").Router();
const mongoUtil = require('../mongoUtil');
const verify = require('./token');
var collection;


// getDistinctSchools
router.get("/School", verify.verToken, (req, res) => {
    collection = mongoUtil.getDept();
    collection.distinct("School", function(error, result){
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getMajors
router.get("/Major", verify.verToken, (req, res) => {
    collection = mongoUtil.getDept();
    collection.find({'Plan Type': 'Major'}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

//getMajorsbySchool
router.get("/Major/:school", verify.verToken, (req, res) => {
    collection = mongoUtil.getDept();
    var name = req.params.school;
    collection.find({'Plan Type': 'Major', 'School': name}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

// getMinors
router.get("/Minor", verify.verToken, (req, res) => {
    collection = mongoUtil.getDept();
    collection.find({'Plan Type': 'Minor'}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

//getMinorsbySchool
router.get("/Minor/:school", verify.verToken, (req, res) => {
    collection = mongoUtil.getDept();
    var name = req.params.school
    collection.find({'Plan Type': 'Minor', 'School': name}).project({'Acad Plan': 1, _id:0}).toArray((error, result) => {
        if(error) {
            return res.status(500).send(error);
        }
        res.send(result);
    });
});

module.exports = router;