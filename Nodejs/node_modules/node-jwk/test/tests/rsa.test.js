const publicKS = require('../data/publicKeySet.json');
const privateKS = require('../data/privateKeySet.json');

const JWKSet = require('../../lib/JWKSet');

const expect = require('chai').expect;

describe('RSA key', () => {

	it('should be initialized from public key objects', () => {

		const keySet = JWKSet.fromObject(publicKS);
		const jwk = keySet.findKeyById('2011-04-29');

		expect(keySet.keys).to.satisfy(k => /(?!.*_invalid)$/.test(k.kid));

	});

	it('should be initialized from private key objects', () => {

		const keySet = JWKSet.fromObject(privateKS);
		const jwk = keySet.findKeyById('2011-04-29');

		expect(jwk.kid).to.be.equal('2011-04-29');
		expect(jwk.key.hasPrivateKey).to.be.true;

		const pubKey = jwk.key.toPublicKeyPEM();
		expect(pubKey).to.be.equal(`-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0vx7agoebGcQSuuPiLJX
ZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tS
oc/BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ/2W+5JsGY4Hc5n9yBXArwl93lqt
7/RN5w6Cf0h4QyQ5v+65YGjQR0/FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0
zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt+bFTWhAI4vMQFh6WeZu0f
M4lFd2NcRwr3XPksINHaQ+G/xBniIqbw0Ls1jF44+csFCur+kEgU8awapJzKnqDK
gwIDAQAB
-----END PUBLIC KEY-----`);

	});

	it('should be initialized from private key objects', () => {

		const keySet = JWKSet.fromObject(privateKS);
		const jwk = keySet.findKeyById('2011-04-29');

		const pubKey = jwk.key.toPublicKeyPEM();
		expect(pubKey).to.be.equal(`-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0vx7agoebGcQSuuPiLJX
ZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tS
oc/BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ/2W+5JsGY4Hc5n9yBXArwl93lqt
7/RN5w6Cf0h4QyQ5v+65YGjQR0/FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0
zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt+bFTWhAI4vMQFh6WeZu0f
M4lFd2NcRwr3XPksINHaQ+G/xBniIqbw0Ls1jF44+csFCur+kEgU8awapJzKnqDK
gwIDAQAB
-----END PUBLIC KEY-----`);

	});

});
