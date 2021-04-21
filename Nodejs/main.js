const crypto = require('crypto');
const { V1 } = require('paseto');
const token = 'v1.public.eyJ1cm46ZXhhbXBsZTpjbGFpbSI6ImZvbyIsImlhdCI6IjIwMTktMDctMDJUMTQ6MDI6MjIuNDg5WiIsImV4cCI6IjIwMTktMDctMDJUMTY6MDI6MjIuNDg5WiIsImF1ZCI6InVybjpleGFtcGxlOmNsaWVudCIsImlzcyI6Imh0dHBzOi8vb3AuZXhhbXBsZS5jb20ifbCaLu19MdLxjrexKh4WTyKr6UoeXzDly_Po1ZNv4wD5CglfY84QqQYTGXLlcLAqZagM3cWJn6xge-lBlT63km6OtOsiWTaKOnYg4MBtQTKmLsjpehpPtDSl_39h2BenB-r911qjYwNNuaRukjrtSVKQtfxdoAoFKEz_eulsDTclEBV7bJrL9Bo0epkJhFShZ6-K8qNd6rTg6Q3YOZCheW1FqNjqfoUYJ9nqPZl2OVbcPdAW3HBeLJefmlL_QGVSRClE2MXOVDrcyf7vGZ0SIj3ylnr6jmEJpzG8o0ap7FblQZI3xp91e-gmw30o6njhSq1ZVWpLqp7FYzq0pknJzGE';



const password = crypto.pseudoRandomBytes(25).toString('base64');
var val = "";

const rsaKeys = crypto.generateKeyPairSync('rsa', {
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

const key = crypto.createPublicKey({key: rsaKeys.publicKey,
    format: 'pem',
    type: 'spki'});


const pkey = crypto.createPrivateKey({key: rsaKeys.privateKey,
    format: 'pem',
    type: 'pkcs8',
    passphrase: password})

const payload = {
  'urn:example:claim': 'foo'
};

// Create token
(async () => {
    val = await V1.sign(payload, pkey, {
      audience: 'urn:example:client',
      issuer: 'https://op.example.com',
      expiresIn: '2 hours'
    })
    console.log(val)
    // v1.public.eyJ1cm46ZXhhbXBsZTpjbGFpbSI6ImZvbyIsImlhdCI6IjIwMTktMDctMDJUMTQ6MDI6MjIuNDg5WiIsImV4cCI6IjIwMTktMDctMDJUMTY6MDI6MjIuNDg5WiIsImF1ZCI6InVybjpleGFtcGxlOmNsaWVudCIsImlzcyI6Imh0dHBzOi8vb3AuZXhhbXBsZS5jb20ifbCaLu19MdLxjrexKh4WTyKr6UoeXzDly_Po1ZNv4wD5CglfY84QqQYTGXLlcLAqZagM3cWJn6xge-lBlT63km6OtOsiWTaKOnYg4MBtQTKmLsjpehpPtDSl_39h2BenB-r911qjYwNNuaRukjrtSVKQtfxdoAoFKEz_eulsDTclEBV7bJrL9Bo0epkJhFShZ6-K8qNd6rTg6Q3YOZCheW1FqNjqfoUYJ9nqPZl2OVbcPdAW3HBeLJefmlL_QGVSRClE2MXOVDrcyf7vGZ0SIj3ylnr6jmEJpzG8o0ap7FblQZI3xp91e-gmw30o6njhSq1ZVWpLqp7FYzq0pknJzGE
  })();

/*

// Verify token
  (async () => {
    await V1.verify(token, key, {
      audience: 'urn:example:client',
      issuer: 'https://op.example.com',
      clockTolerance: '1 min',
    })
    // {
    //   'urn:example:claim': 'foo',
    //   iat: '2019-07-02T14:02:22.489Z',
    //   exp: '2019-07-02T16:02:22.489Z',
    //   aud: 'urn:example:client',
    //   iss: 'https://op.example.com'
    // }
  })();
*/