
import string

tags = [
    "general",
    "danger",
    "local",
    "update"
]

localityReferences = [
    "near",
    "around",
    "at"
]

def formatText(text):
    text = str(text)
    text = text.lower().rstrip().lstrip()
    for punc in string.punctuation:
        text = text.replace(punc, " ")
    return text

def parseMessage(incomingMessage):
    formattedMessage = formatText(incomingMessage)
    words = formattedMessage.split(" ")
    pMessage = ParsedMessage()
    if words[0] in tags:
        pMessage.setTag(words[0])
        messageStr = str()
        for i, word in enumerate(words[1:]):
            if word in localityReferences:
                try:
                    locationDescriptor = " ".join(words[i + 2:])
                    if not locationDescriptor.rstrip().lstrip() == "":
                        pMessage.setLocationDescriptor(locationDescriptor)
                except IndexError:
                    pass
                break
            else:
                messageStr += word + " "
        pMessage.setMessage(messageStr)
        return pMessage
    else:
        return None

class ParsedMessage(object):

    def __init__(self):
        self.tag = None
        self.message = None
        self.locationDescriptor = None

    def setTag(self, tag):
        self.tag = tag
        return self

    def setMessage(self, message):
        self.message = message
        return self

    def setLocationDescriptor(self, locationDescriptor):
        self.locationDescriptor = locationDescriptor
        return self

    def getTag(self):
        return self.tag

    def getMessage(self):
        return self.message

    def getLocationDescriptor(self):
        return self.locationDescriptor

    def __str__(self):
        return (
            "Tag: " + self.tag + "\n" +
            "Message: " + str(self.message) + "\n" +
            "Location Descriptor: " + str(self.locationDescriptor)
        )

""" Test Functions """
def test_parseMessage():
    message = (
        "danger there is a rebel army " +
        "coming this way near the awesome village"
    )

    # message = "local hey everybody near"
    print "Message:", message
    pm = parseMessage(message)
    print pm

if __name__ == "__main__":
    test_parseMessage()


