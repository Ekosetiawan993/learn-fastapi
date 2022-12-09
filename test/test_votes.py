from app import schemas, models
import pytest


@pytest.fixture()
def test_vote(create_user, create_posts, session):
    new_vote = models.Vote(
        post_id=create_posts[2].id, user_id=create_user['id'])
    session.add(new_vote)
    session.commit()


def test_on_vote_success(authorized_client, create_posts):
    response = authorized_client.post(
        '/vote/', json={'post_id': create_posts[2].id, 'dir': 1})

    assert response.status_code == 201


def test_vote_twice(authorized_client, create_posts, test_vote):
    response = authorized_client.post(
        '/vote/', json={'post_id': create_posts[2].id, 'dir': 1})

    assert response.status_code == 409


def test_delete_vote(authorized_client, create_posts, test_vote):
    response = authorized_client.post(
        '/vote/', json={'post_id': create_posts[2].id, 'dir': 0})

    assert response.status_code == 201


def test_delete_not_exist_vote(authorized_client, create_posts):
    response = authorized_client.post(
        '/vote/', json={'post_id': create_posts[2].id, 'dir': 0})

    assert response.status_code == 404


def test_vote_not_exist_posts(authorized_client, create_posts):
    response = authorized_client.post(
        '/vote/', json={'post_id': 88888, 'dir': 0})

    assert response.status_code == 404


def test_unauthenticated_user_vote(client, create_posts):
    response = client.post(
        '/vote/', json={'post_id': 88888, 'dir': 1})

    assert response.status_code == 401
