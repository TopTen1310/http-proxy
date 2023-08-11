import pytest
import re
from aiohttp import request as make_request
from proxy.settings import JWT_HEADER_NAME, URL_NOTATION, HOST_PORT


def get_proxy_url(path):
    return URL_NOTATION.format(
        scheme="http", host="proxy", port=HOST_PORT, path=path
    )


@pytest.mark.asyncio
async def test_status_route():
    expected_url = get_proxy_url('status')

    async with make_request(method='GET', url=expected_url) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert 'processed_requests' in data
        assert 'uptime' in data


@pytest.mark.asyncio
async def test_increment_request():
    test_path_url = get_proxy_url('post')
    status_url = get_proxy_url('status')

    # Making the POST request
    async with make_request(method="POST", url=test_path_url):
        pass

    # Checking the status
    async with make_request(method='GET', url=status_url) as resp:
        data = await resp.json()
        assert data['processed_requests'] == 1


@pytest.mark.asyncio
async def test_uptime_format():
    status_url = get_proxy_url('status')

    async with make_request(method='GET', url=status_url) as resp:
        data = await resp.json()
        uptime_pattern = re.compile(r"(\d+d )?(\d+h )?(\d+m )?(\d+s)")
        assert uptime_pattern.match(data['uptime'])


@pytest.mark.asyncio
async def test_forwarding_to_upstream():
    test_path_url = get_proxy_url('post')

    async with make_request(method="POST", url=test_path_url) as resp:
        assert resp.status == 200
        data = await resp.json()
        assert data['url'] == "https://proxy/post"


@pytest.mark.asyncio
async def test_jwt_header_forwarding():
    test_path_url = get_proxy_url('post')

    async with make_request(method="POST", url=test_path_url) as resp:
        data = await resp.json()
        assert JWT_HEADER_NAME in data['headers']
