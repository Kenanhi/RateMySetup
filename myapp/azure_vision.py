import logging
import os
from typing import List, Any

logger = logging.getLogger(__name__)


def analyze_hardware_tags(image_file: Any) -> List[str]:
    """
    Extract hardware and visual tags from an image using Azure Computer Vision.

    Uses ImageAnalysisClient and VisualFeatures.TAGS.
    Gracefully degrades to an empty list [] if credentials are missing or the API call fails.
    """
    endpoint = os.getenv('AZURE_VISION_ENDPOINT') or os.getenv('AZURE_COMPUTER_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY') or os.getenv('AZURE_COMPUTER_VISION_KEY')

    if not endpoint or not key:
        logger.warning(
            "Azure Vision credentials not configured (AZURE_VISION_ENDPOINT / AZURE_VISION_KEY). "
            "Returning empty tags list."
        )
        return []

    if not image_file:
        return []

    try:
        from azure.ai.vision.imageanalysis import ImageAnalysisClient
        from azure.ai.vision.imageanalysis.models import VisualFeatures
        from azure.core.credentials import AzureKeyCredential

        # Extract image bytes and ensure stream pointer is safely restored
        image_bytes: bytes = b""
        if hasattr(image_file, 'read'):
            image_bytes = image_file.read()
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
        elif isinstance(image_file, (bytes, bytearray)):
            image_bytes = bytes(image_file)
        else:
            logger.warning("Unsupported image data type: %s", type(image_file))
            return []

        if not image_bytes:
            return []

        client = ImageAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        result = client.analyze(
            image_data=image_bytes,
            visual_features=[VisualFeatures.TAGS]
        )

        tags: List[str] = []
        if result.tags is not None:
            tag_items = getattr(result.tags, 'list', result.tags)
            for item in tag_items:
                name = getattr(item, 'name', None)
                if name is None and isinstance(item, dict):
                    name = item.get('name')
                if name:
                    tags.append(str(name))

        logger.info("Azure Computer Vision detected %d tags: %s", len(tags), tags)
        return tags

    except Exception as exc:
        logger.error("Azure Computer Vision analysis failed: %s", exc, exc_info=True)
        # Attempt to reset stream pointer if it was read
        if hasattr(image_file, 'seek'):
            try:
                image_file.seek(0)
            except Exception:
                pass
        return []
