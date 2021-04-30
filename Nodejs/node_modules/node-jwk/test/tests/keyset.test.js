const publicKS = require('../data/publicKeySet.json');
const privateKS = require('../data/privateKeySet.json');

const JWKSet = require('../../lib/JWKSet');

const expect = require('chai').expect;

describe('JWKSet', () => {

	it('should be initialized from public key objects', () => {

		const keySet = JWKSet.fromObject(publicKS);
		expect(keySet.keys).to.satisfy(k => /(?!.*_invalid)$/.test(k.kid));

	});

	it('should be initialized from private key objects', () => {

		const keySet = JWKSet.fromObject(privateKS);
		expect(keySet.keys).to.satisfy(k => /(?!.*_invalid)$/.test(k.kid));

	});

});
