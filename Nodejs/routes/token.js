const paseto = require('paseto');
const { V2: { sign } } = paseto;
const { V2: { verify } } = paseto;
const crypto = require('crypto');

const password = crypto.pseudoRandomBytes(25).toString('base64');
const payload = {'urn:example:claim': 'DB Access'};

const rsaKeys = crypto.generateKeyPairSync('ed25519', {
    modulusLength: 2048,
    publicKeyEncoding: {
        type: 'spki',
        format: 'pem',
    },
    privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
        cipher: 'aes-256-cbc',
        passphrase: password,
    }
});

const privkey = crypto.createPrivateKey({key: rsaKeys.privateKey,
    format: 'pem',
    type: 'pkcs8',
    passphrase: password});

const pubkey = crypto.createPublicKey({key: rsaKeys.publicKey,
    format: 'pem',
    type: 'spki'});

module.exports = {
    genToken: async () => {
        const token = await sign(payload, privkey);
        return token;
    },
    verToken: async (req, res, next) => {
        const token = req.header('auth-token');
        if(!token) return res.status(401).send('Access Denied');
        try{
            const verified = await verify(String(token), pubkey);
            next();
        } catch (err){
            res.status(400).send('Invalid Token');
        }
    }
}