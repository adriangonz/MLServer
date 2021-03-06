from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute as FastAPIRoute
from fastapi.responses import ORJSONResponse

from .endpoints import Endpoints
from .requests import ORJSONRequest

from ..settings import Settings
from ..handlers import DataPlane


class APIRoute(FastAPIRoute):
    """
    Custom route to use ORJSONRequest handler.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = ORJSONRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


def create_app(settings: Settings, data_plane: DataPlane) -> FastAPI:
    endpoints = Endpoints(data_plane)
    routes = [
        APIRoute("/v2/health/live", endpoints.live),
        APIRoute("/v2/health/ready", endpoints.ready),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/ready",
            endpoints.model_ready,
        ),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/infer",
            endpoints.infer,
            methods=["POST"],
        ),
    ]

    app = FastAPI(
        debug=settings.debug, routes=routes, default_response_class=ORJSONResponse
    )

    return app
