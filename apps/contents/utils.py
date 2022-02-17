from .models import Pages


def validateKeys(payload, requiredKeys):
    # extract keys from payload
    payloadKeys = list(payload.keys())

    # check if extracted keys is present in requiredKeys
    missingKeys = []
    for key in requiredKeys:
        if key not in payloadKeys:
            missingKeys.append(key)

    return missingKeys


def getPageBySlug(slug):
    try:
        return Pages.objects.get(slug=slug)
    
    except Pages.DoesNotExist:
        return None


def getPageByTitle(title):
    try:
        return Pages.objects.get(title=title)
    
    except Pages.DoesNotExist:
        return None
