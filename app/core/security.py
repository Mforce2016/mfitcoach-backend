from fastapi import Header, HTTPException
from firebase_admin import auth


def verify_firebase_token(
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Token requerido"
        )

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        decoded_token = auth.verify_id_token(token)

        return decoded_token


    except Exception as e:

        print("ERROR FIREBASE:", str(e))

        raise HTTPException(

            status_code=401,

            detail=f"Token inválido: {str(e)}"

        )