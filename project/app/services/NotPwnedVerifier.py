import hashlib, requests # pragma: no cover


class NotPwnedVerifier: # pragma: no cover
    def verify(self, data: str, threshold: int = 0):

        sha1_hash = hashlib.sha1(data.encode())
        hash_prefix = sha1_hash[:5]

        self.search(hash_prefix)
        if len(data) == 0:
            return False

    def search(self, hash_prefix: str):
        try:
            response = requests.get(
                "https://api.pwnedpasswords.com/range/{0}".format(hash_prefix)
            )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
        # chech if request was successful
        # explode using `:`
