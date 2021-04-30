const publicKS = require('../data/publicKeySet.json');
const privateKS = require('../data/privateKeySet.json');

const JWKSet = require('../../lib/JWKSet');

const expect = require('chai').expect;

describe('EC key', () => {

	it('should be initialized from public key objects', () => {

		const keySet = JWKSet.fromObject(publicKS);
		const jwk = keySet.findKeyById('k1');

		expect(jwk.kid).to.be.equal('k1');
		expect(jwk.key.hasPrivateKey).to.be.false;

		const pubKey = jwk.key.toPublicKeyPEM();
		expect(pubKey).to.be.equal(`-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEJ41kktcqHeQYVdFMlv6AorbqOlmQ
ESJqR4ZKiozpw0Lte4nZ4bm5uzeImkKvHADS+iBxSoBJGXyR7OOkh8dFvg==
-----END PUBLIC KEY-----`);

	});

	it('should be initialized from private key objects', () => {

		const keySet = JWKSet.fromObject(privateKS);
		const jwk = keySet.findKeyById('k5');

		expect(jwk.kid).to.be.equal('k5');
		expect(jwk.key.hasPrivateKey).to.be.true;

		const pubKey = jwk.key.toPublicKeyPEM();
		expect(pubKey).to.be.equal(`-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEMKBCTNIcKUSDii11ySs3526iDZ8A
iTo7Tu6KPAqv7D7gS2XpJFbZiItSs3m9+9Ue6GnvHw/GW2ZZaVtszggXIw==
-----END PUBLIC KEY-----`);

	const privKey = jwk.key.toPrivateKeyPEM();
	expect(privKey).to.be.equal(`-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIPO9DAeoH7kyeB7VJ1L2DMiaa+XlGTT+AZON21XY93gBoAoGCCqGSM49
AwEHoUQDQgAEMKBCTNIcKUSDii11ySs3526iDZ8AiTo7Tu6KPAqv7D7gS2XpJFbZ
iItSs3m9+9Ue6GnvHw/GW2ZZaVtszggXIw==
-----END EC PRIVATE KEY-----`);

	});

});
