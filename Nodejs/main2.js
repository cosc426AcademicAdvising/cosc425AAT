

const crypto = require('crypto')
const { V2 } = require('paseto')

const password = crypto.pseudoRandomBytes(25).toString('base64');
var val = "";
const payload = {
  'urn:example:claim': 'foo'
}

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

const pkey = crypto.createPrivateKey({key: rsaKeys.privateKey,
    format: 'pem',
    type: 'pkcs8',
    passphrase: password});


(async () => {
  const token = await V2.sign(payload, pkey, {
    audience: 'urn:example:client',
    issuer: 'https://op.example.com',
    expiresIn: '2 hours'
  })
  console.log(token)
  // v2.public.eyJ1cm46ZXhhbXBsZTpjbGFpbSI6ImZvbyIsImlhdCI6IjIwMTktMDctMDJUMTM6MzY6MTIuMzgwWiIsImV4cCI6IjIwMTktMDctMDJUMTU6MzY6MTIuMzgwWiIsImF1ZCI6InVybjpleGFtcGxlOmNsaWVudCIsImlzcyI6Imh0dHBzOi8vb3AuZXhhbXBsZS5jb20ifZfV2b1K3xbn8Az3aL24aPtqGRQ3dOf7DP3_GijBekGC2038REYwcyo1rv5o7OOjPuQ7-SqKhPKx0fn6hwm4nAw
})();


/*
const token = 'v2.public.eyJ1cm46ZXhhbXBsZTpjbGFpbSI6ImZvbyIsImlhdCI6IjIwMTktMDctMDJUMTM6MzY6MTIuMzgwWiIsImV4cCI6IjIwMTktMDctMDJUMTU6MzY6MTIuMzgwWiIsImF1ZCI6InVybjpleGFtcGxlOmNsaWVudCIsImlzcyI6Imh0dHBzOi8vb3AuZXhhbXBsZS5jb20ifZfV2b1K3xbn8Az3aL24aPtqGRQ3dOf7DP3_GijBekGC2038REYwcyo1rv5o7OOjPuQ7-SqKhPKx0fn6hwm4nAw';

const key = crypto.createPrivateKey({key: rsaKeys.publicKey,
    format: 'pem',
    type: 'spki'});

(async () => {
    await V2.verify(token, key, {
      audience: 'urn:example:client',
      issuer: 'https://op.example.com',
      clockTolerance: '1 min'
    })
    // {
    //   'urn:example:claim': 'foo',
    //   iat: '2019-07-02T13:36:12.380Z',
    //   exp: '2019-07-02T15:36:12.380Z',
    //   aud: 'urn:example:client',
    //   iss: 'https://op.example.com'
    // }
  })()
  */