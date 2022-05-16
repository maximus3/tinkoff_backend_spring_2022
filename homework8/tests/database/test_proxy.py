import pytest

from tests.static import user_proxy_data


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_eq_error(prepare_db_user_env, model, parameters):
    assert not model.get(**parameters) == 1


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_create_error_no_such_param(prepare_db_env, model, parameters):
    with pytest.raises(TypeError):
        model.create(no_param='no_param')


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_create(prepare_db_env, model, parameters):
    model.create(**parameters)
    assert model.get(**parameters) is not None


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_get_none(prepare_db_env, model, parameters):
    assert model.get(**parameters) is None


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_get_expect(prepare_db_user_env, model, parameters):
    assert model.get_expect(**parameters)


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_get_model(
    prepare_db_user_env, create_session, model, parameters
):
    assert model.get_model(**parameters)
    with create_session() as session:
        assert model(
            model.get_model(**parameters, session=session)
        ) == model.get_expect(**parameters)


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_get_all(prepare_db_user_env, model, parameters):
    assert model.get_all(**parameters) == [model.get_expect(**parameters)]


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_update_none(prepare_db_user_env, model, parameters):
    proxy_model = model.get(**parameters)
    proxy_model.id = -1
    assert proxy_model.update(**parameters) is None


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_update_no_attr(prepare_db_user_env, model, parameters):
    proxy_model = model.get(**parameters)
    parameters['no_such_parameter'] = 'no_such_parameter'
    assert proxy_model.update(**parameters) is None


@pytest.mark.parametrize(
    ('model', 'parameters'),
    [
        user_proxy_data(),
    ],
)
def test_proxy_update(prepare_db_user_env, model, parameters):
    assert model.get(**parameters).update(**parameters) == model.get(
        **parameters
    )
