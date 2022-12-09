from app import schemas
import pytest


def test_get_all_posts(authorized_client, create_posts):
    response = authorized_client.get('/posts/')
    print('uda muncul belum postnya?')
    print(response.json())

    assert len(response.json()) == len(create_posts)
    assert response.status_code == 200


def test_unauthorized_get_all_posts(client, create_posts):
    response = client.get('/posts/')

    assert response.status_code == 401


def test_unauthorized_get_one_post(client, create_posts):
    response = client.get(f'/posts/{create_posts[0].id}')

    assert response.status_code == 401


def test_one_post_not_exist(authorized_client, create_posts):
    response = authorized_client.get(f'/posts/888')

    assert response.status_code == 404


def test_get_one_post(authorized_client, create_posts):
    response = authorized_client.get(f'/posts/{create_posts[0].id}')
    print(response.json())
    post = schemas.PostVote(**response.json())

    # print(post)
    assert post.Post.id == create_posts[0].id
    assert post.Post.content == create_posts[0].content
    assert response.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ('first titlee', 'awesome first content', True),
    ('seconddddd titlee', 'awesome first content', False),
    ('thirdddd titlee', 'awesome first content', True),
])
def test_creating_posts(authorized_client, create_user, create_posts, title, content, published):
    response = authorized_client.post(
        '/posts/', json={'title': title, 'content': content, 'published': published})

    created_post = schemas.PostContent(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.user_id == create_user['id']


def test_default_published_true(authorized_client, create_user, create_posts):
    response = authorized_client.post(
        '/posts/', json={'title': 'title', 'content': 'content'})

    created_post = schemas.PostContent(**response.json())
    assert response.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content'
    assert created_post.user_id == create_user['id']
    assert created_post.published == True


def test_default_published_false(authorized_client, create_user, create_posts):
    response = authorized_client.post(
        '/posts/', json={'title': 'title', 'content': 'content', 'published': False})

    created_post = schemas.PostContent(**response.json())
    assert response.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content'
    assert created_post.user_id == create_user['id']
    assert created_post.published == False


def test_unauthorized_create_post(client, create_posts):
    response = client.post(
        '/posts/', json={'title': 'title', 'content': 'content', 'published': False})

    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, create_posts):
    response = client.delete(
        f'/posts/{create_posts[0].id}')

    assert response.status_code == 401


def test_user_success_delete_post(authorized_client, create_posts):
    response = authorized_client.delete(
        f'/posts/{create_posts[0].id}')

    assert response.status_code == 204


def test_delete_not_exist_post(authorized_client, create_posts):
    response = authorized_client.delete(
        f'/posts/88')

    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, create_posts_special_id):
    response = authorized_client.delete(
        f'/posts/{create_posts_special_id[0].id}')

    assert response.status_code == 403


def test_update_post(authorized_client, create_posts):
    data = {
        'title': 'new title',
        'content': 'new unique conntentttttdfsjoig'
    }

    response = authorized_client.put(f'/posts/{create_posts[0].id}', json=data)

    updated_post = schemas.PostContent(**response.json())
    print(updated_post)
    assert response.status_code == 200
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, create_posts):
    data = {
        'title': 'new title',
        'content': 'new unique conntentttttdfsjoig'
    }

    response = authorized_client.put(f'/posts/{create_posts[2].id}', json=data)

    # updated_post = schemas.PostContent(**response.json())
    # print(updated_post)
    assert response.status_code == 403


def test_unauthenticated_user_update_post(client, create_posts):
    data = {
        'title': 'new title',
        'content': 'new unique conntentttttdfsjoig'
    }

    response = client.put(f'/posts/{create_posts[0].id}', json=data)

    assert response.status_code == 401


def test_update_not_exist_post(authorized_client, create_posts):
    data = {
        'title': 'new title',
        'content': 'new unique conntentttttdfsjoig'
    }

    response = authorized_client.put(f'/posts/88888', json=data)

    assert response.status_code == 404
