import jwt


class JWT:

    def encode(
        payload: dict,
        private_key: str,
        algorithm: str,
    ):
        return jwt.encode(
            payload=payload,
            key=private_key,
            algorithm=algorithm,
        )

    def decode(
        token: str | bytes,
        public_key: str,
        algorithm: list[str],
    ):
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=algorithm,
        )
