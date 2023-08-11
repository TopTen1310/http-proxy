import logging
from aiohttp import web, ClientSession
from proxy.settings import (
    JWT_HEADER_NAME, UPSTREAM_IP_OR_FQDN, UPSTREAM_PORT,
    UPSTREAM_SCHEME, URL_NOTATION
)
from .jwt_manager import JWTManager
from .status_manager import StatusManager

# Setting up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ProxyServer:
    def __init__(self):
        self.app = web.Application()
        self.status_manager = StatusManager()

        # Attach instance of ProxyServer to app for routes to access
        self.app["proxy_server"] = self

        # Setup routes
        self.setup_routes()

        self.app.on_cleanup.append(on_cleanup)

    def setup_routes(self):
        """Configures the routes for the application."""
        self.app.router.add_route("GET", "/status", self.status)
        self.app.router.add_route("POST", "/{path:.*}", self.handle)

    @StatusManager.increment_request
    async def handle(self, request: web.Request) -> web.Response:
        """
        Handles the request, generates a JWT token, and forwards the request to the upstream URL.

        Args:
            request (web.Request): The incoming request.

        Returns:
            web.Response: The response from the upstream URL.
        """
        logger.info("Handling request...")

        token = JWTManager.generate_token()

        # Constructing the upstream URL
        upstream_url = URL_NOTATION.format(
            scheme=UPSTREAM_SCHEME,
            host=UPSTREAM_IP_OR_FQDN,
            port=UPSTREAM_PORT,
            path=request.match_info['path']
        )

        # Collect headers
        headers = {k: v for k, v in request.headers.items()}
        headers[JWT_HEADER_NAME] = token

        try:
            async with ClientSession() as session:
                # Forward the incoming request method, headers, and body to the upstream server
                async with session.request(
                    method=request.method,
                    url=upstream_url,
                    headers=headers,
                    data=await request.read() if request.can_read_body else None
                ) as resp:
                    # Return the upstream response content, headers, and status to the client
                    return web.Response(
                        text=await resp.text(),
                        headers=resp.headers,
                        status=resp.status
                    )

        except Exception as e:
            logger.error(f"Error while processing request: {e}")
            return web.Response(text="Internal Server Error", status=500)

    async def status(self, request: web.Request) -> web.Response:
        """
        Returns the server's status.

        Args:
            request (web.Request): The incoming request.

        Returns:
            web.Response: JSON response containing server status details.
        """
        logger.info("Fetching status...")

        return web.json_response(self.status_manager.get_status())

    def run(self):
        logger.info(f"Server started at {self.status_manager.start_time}")
        web.run_app(self.app)


async def on_cleanup(app):
    await app["session"].close()


def run_app() -> None:
    """Initializes and starts the proxy server."""
    server = ProxyServer()
    server.run()
