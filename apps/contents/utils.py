from .models import Pages


def validate_keys(payload, required_keys):
    # extract keys from payload
    payload_keys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missing_keys = []
    for key in required_keys:
        if key not in payload_keys:
            missing_keys.append(key)

    return missing_keys


def get_page_by_slug(slug):
    try:
        return Pages.objects.get(slug=slug)
    
    except Pages.DoesNotExist:
        return None


def get_page_by_title(title):
    try:
        return Pages.objects.get(title=title)
    
    except Pages.DoesNotExist:
        return None
