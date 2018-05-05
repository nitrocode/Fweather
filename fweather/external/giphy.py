import giphy_client
from giphy_client.rest import ApiException
import os
import dotenv
import random
import logging

PARAMS = {
    'api_key': os.getenv('giphy'),
    'limit': 25,
    'offset': 0,
    'rating': 'g',
    'lang': 'en',
    'fmt': 'json',
}

API_INSTANCE = giphy_client.DefaultApi()


def get_random_giphy(query):
    """Return a random gif based on the 25 items returned on the query.

    :param query: search for anything
    :return: url to a gif to embed in an email
    """
    params = PARAMS.copy()
    params['q'] = query
    try:
        api_response = API_INSTANCE.gifs_search_get(**params)
        return random.sample(api_response.data, 1)[0].images.original.url
    except ApiException as e:
        logging.error("Exception calling giphy's search_get: {}".format(e))


if __name__ == '__main__':
    dotenv.read_dotenv('../../.env')
    PARAMS['api_key'] = os.getenv('giphy')
    logging.info(get_random_giphy('partly raining'))
