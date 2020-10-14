from django.conf import settings
from django.utils.translation import get_language


def yandex_maps(request):
    lang = get_language()
    api_version = getattr(settings, "YANDEX_MAPS_API_VERSION", "2.1")
    try:
        api_key = getattr(settings, "YANDEX_MAPS_API_KEY")
    except AttributeError as err:
        raise Exception(
            f"{__name__}.yandex_maps context processor requires YANDEX_MAPS_API_KEY is declared in projects settings"
        ) from err
    api_script_url = f"https://api-maps.yandex.ru/{api_version}/?apikey={api_key}&lang={lang}"
    api_script = f'<script src="{api_script_url}" type="text/javascript"></script>'
    return {
        "yandex_maps": {
            "api_key": api_key,
            "api_script_url": api_script_url,
            "api_script": api_script
        }
    }
