from fastapi import HTTPException, status


def unauth_error(detail: str, auth_type: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": auth_type},
    )


def server_error(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


def invalid_data(detail: str):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
