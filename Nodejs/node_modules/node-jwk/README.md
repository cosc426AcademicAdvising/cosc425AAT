# node-jwk

Implementation of RFC-7517 (JSON Web Key) compliant key handling.

The module can be used to convert keys into buffers or other formats to
enable the direct use of JWK formatted keys with other node modules like
[njwt](https://www.npmjs.com/package/njwt) and others.

## Usage

The module offers the classes `JWK` and `JWKSet` to work with JWK encoded keys
or key sets.

You can instantiate either of the objects from a stringified JSON or an object.
```
const njwk = require('node-jwk');

const myKey = njwk.JWK.fromJSON(myJSONString);
const myKeySet = njwk.JWKSet.fromObject(myKeySet);
```

### Keysets (JWKSet)

Keysets can contain a number of different keys which are unique by their _kid_.

#### JWKSet.findKeyById(kid)

The JWKSet class offers the `findKeyById` method that will let you grab a key
by its id and returns it wrapped in a JWK object.

#### JWKSet.findKeysByUse(use)

There might be cases where you want to use a key designated for encoding/decoding or
signing/verification. With `findKeysByUse` you can retrieve an array of all
contained keys that match the use given.

But remember that the use property is specified as OPTIONAL, so is the content of
it. Be prepared that keys you get from 3rd party could miss it.

#### JWKSet.keys

Returns all keys as an array of JWK objects.

#### JWKSet.fromObject(object) JWKSet.fromJSON(string)

Factory to instantiate JWKSet objects. This method will throw on invalid
keysets (the keyset structure or invalid JSON). According to the specification
(RFC) invalid keys contained in a valid set are ignored.


### Keys (JWK)

All standard JWK properties are exposed by the JWK object. Be aware that per
specification all properties but `kty` and `kid` are optional. Here's a list:
```
	kid
	kty
	use
	key_ops
	alg
```

#### JWK.key

Through the key property you can access the key algorithm specific functionality.

##### JWK.key.hasPrivateKey

Returns true if the key contains a private key part.

##### JWK.key.toPublicKeyPEM() => String

Generates a PEM that contains the public key of the JWK. This can be used
directly as key in OpenSSL or other node modules and works for EC as well as
RSA keys.

##### JWK.key.toPrivateKeyPEM() => String

Generates a PEM that contains the private key of the JWK. This can be used
directly as key in OpenSSL or other node modules and works for EC as well as
RSA keys.

#### JWK.fromObject(object) JWK.fromJSON(string)

Factory to instantiate JWK objects. This method will throw on invalid
keys (the keyset structure or invalid JSON).
Normally you should use keysets to manage your keys instead of single keys.


## Examples

### Creating a signed token with node-jwk and njwt

The example uses bluebird promises to be able to catch exceptions thrown in the
key retrieval and lodash for convenience.

```
const time = Math.floor(_.now() / 1000);

const claims = {
	iss: 'itsME',
	aud: 'myAudience',
	iat: time,
	exp: time + 3600
};

return BbPromise.try(() => {
	const keySet = nodeJWK.JWKSet.fromObject(myPrivateKeySet);
	const jwk = keySet.findKeyById(myKeyId);

	if (!jwk) {
		return BbPromise.reject(new Error('Huh, my key is not there...'));
	}

	const keyPEM = jwk.key.toPrivateKeyPEM();
	const jwt = njwt.create(claims, keyPEM, jwk.alg);

	return BbPromise.resolve(jwt.compact());
})
.catch(err => {
	return BbPromise.reject(err);
});
```

## Supported key types

RSA, EC, oct

All keys but binary (oct) keys can be converted into PEM format for their
public and private keys.

## References

[RFC-7517 JSON Web Key](https://tools.ietf.org/html/rfc7517)

[RFC-7518 JSON Web Algorithms](https://tools.ietf.org/html/rfc7518)
