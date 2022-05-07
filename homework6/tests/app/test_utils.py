from app import utils


def test_image_decode(images_data, images):
    for size in images_data:
        assert (
            utils.ImageEncoder.decode(images_data[size]).tobytes()
            == images[size].tobytes()
        )


def test_image_encode(images_data, images):
    for size in images_data:
        assert utils.ImageEncoder.encode(images[size]) == images_data[size]


def test_image_process_return(image_data, images_data):
    result = utils.ImageProcessor.process(0, image_data, True)
    for size in images_data:
        assert result[size] == images_data[size]


def test_image_process(image_data, images_data, fake_redis):
    utils.ImageProcessor.process(0, image_data)
    result = fake_redis.hgetall(0)
    for size in result:
        assert result[size].decode() == images_data[size.decode()]
