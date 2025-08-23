from src.process_media.image.image_options import ImageVariant
from typing import NamedTuple, Dict
from src.process_media.common import Vector2Int

class PathChecker(NamedTuple):
    pathRegex:str|None=None
    bucket:str|None=None

class VariantRoute(NamedTuple):
    path:PathChecker
    config:ImageVariant

VariantsSchema=Dict[str,VariantRoute]

variantsSchema={
    "avatar_thumbnail":VariantRoute(
        PathChecker(
            bucket="public",
            pathRegex=r"users\/[^\/]+\/profile\/avatar"
        ),
        ImageVariant(
            limit_resolution=Vector2Int(150,150),
            quality=90
        )
    )
}