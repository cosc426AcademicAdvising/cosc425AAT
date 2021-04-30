'use strict';
/**
 * RSA key
 */

const _ = require('lodash');
const base64url = require('base64url');
const asn = require('asn1.js');
const util = require('../util');

const OPTIONAL_PRIVATE_PROPS = [
	'p', 'q', 'dp', 'dq', 'qi'
];

// Define ASN structures
const RSAPrivateKey = asn.define('RSAPrivateKey', function() {
	this.seq().obj(
		this.key('id').int(),
		this.key('n').int(),
		this.key('e').int(),
		this.key('d').int(),
		this.key('p').int(),
		this.key('q').int(),
		this.key('dp').int(),
		this.key('dq').int(),
		this.key('qi').int()
	);
});

const RSAPublicKeyHeader = asn.define('RSAPublicKeyHeader', function() {
	this.seq().obj(
		this.key('keyType').objid({
			'1.2.840.113549.1.1.1': 'RSA'
		}),
		this.null_()
	);
});

const RSAPublicKeyParams = asn.define('RSAPublicKeyParams', function() {
	this.seq().obj(
		this.key('n').int(),
		this.key('e').int()
	);
});

const RSAPublicKey = asn.define('RSAPublicKey', function() {
	this.seq().obj(
		this.key('header').use(RSAPublicKeyHeader),
		this.key('content').bitstr()
	);
});

class RSAKey {

	constructor(n, e, d, p, q, dp, dq, qi, oth, r) {
		this._data = {
			id: 0,
			n: util.unsigned(n),
			e: util.unsigned(e),
			d: util.unsigned(d),
			p: util.unsigned(p),
			q: util.unsigned(q),
			dp: util.unsigned(dp),
			dq: util.unsigned(dq),
			qi: util.unsigned(qi),
			oth: util.unsigned(oth),
			r: util.unsigned(r)
		};
	}

	get hasPrivateKey() {
		return !_.isNil(this._data.d);
	}

	toPublicKeyPEM() {
		const keyParams = RSAPublicKeyParams.encode(this._data, 'der');

		const params = {
			header: {
				keyType: 'RSA'
			},
			content: {
				data: keyParams
			}
		};
		return RSAPublicKey.encode(params, 'pem', { label: 'PUBLIC KEY' });
	}

	toPrivateKeyPEM() {
		if (!this.hasPrivateKey) {
			return null;
		}

		return RSAPrivateKey.encode(this._data, 'pem', { label: 'RSA PRIVATE KEY' });
	}

	static validate(key) {
		// @see RFC-7517 par. 6.3
		let result = _.has(key, 'n') && _.has(key, 'e');

		// RFC-7517 6.3.2:
		// If the producer includes any of the other private key parameters, then
		// all of the others MUST be present, with the exception of "oth"
		result = result &&
			(!_.has(key, 'd') ||
				_.some(OPTIONAL_PRIVATE_PROPS, prop => _.has(key, prop)) && _.every(OPTIONAL_PRIVATE_PROPS, prop => _.has(key, prop)));

		return result;
	}

	static fromKey(key) {
		const n = base64url.toBuffer(key.n);
		const e = base64url.toBuffer(key.e);
		const d = key.d ? base64url.toBuffer(key.d) : null;
		const p = key.p ? base64url.toBuffer(key.p) : null;
		const q = key.q ? base64url.toBuffer(key.q) : null;
		const dp = key.dp ? base64url.toBuffer(key.dp) : null;
		const dq = key.dq ? base64url.toBuffer(key.dq) : null;
		const qi = key.qi ? base64url.toBuffer(key.qi) : null;
		const oth = key.oth ? base64url.toBuffer(key.oth) : null;
		const r = key.r ? base64url.toBuffer(key.r) : null;

		return new RSAKey(n, e, d, p, q, dp, dq, qi, oth, r);
	}

}

module.exports = RSAKey;
