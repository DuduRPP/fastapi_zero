from http import HTTPStatus

from jwt import decode

from fast_zero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_no_user_when_valid_token(client, user, token_no_user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_no_user}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_invalid_user_when_valid_token(client, user, token_invalid_user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_invalid_user}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
