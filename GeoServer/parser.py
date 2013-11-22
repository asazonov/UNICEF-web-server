
import string

tags = [
    "message",
    # available to everybody; sends message to everybody
    # within 15 km or to everybody in the list if the location is not set
    "danger",
    # available to everybody; sends message to everybody within 3 km
    "local",
    "update"
]

localityReferences = [
    "near",
    "around",
    "at"
]

messageRecipients = [
    "teachers",
    "students",
    "everybody"
]

def formatText(text):
    """
    Formats the text to a parseable string
    """

    text = str(text)
    text = text.lower().rstrip().lstrip()
    for punc in string.punctuation:
        text = text.replace(punc, " ")
    return text

def parseMessage(incomingMessage):
    """
    Parses a message into tags, locations, and sending messages
    """

    formattedMessage = formatText(incomingMessage)
    words = formattedMessage.split(" ")
    pMessage = ParsedMessage()
    if words[0] in tags:
        pMessage.setTag(words[0])
        messageStr = str()
        if pMessage.getTag() == "message":
            if words[1] in messageRecipients:
                pMessage.setMessageRecipients(words[1])
                pMessage.setMessage(" ".join(words[2:]))
                return pMessage
            else:
                return None
        elif pMessage.getTag() == "update":
            pMessage.setLocationDescriptor(" ".join(words[1:]))
        else:
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
        self.messageRec = None

    def setTag(self, tag):
        self.tag = tag
        return self

    def setMessage(self, message):
        self.message = message
        return self

    def setMessageRecipients(self, messageRec):
        self.messageRec = messageRec
        return self

    def setLocationDescriptor(self, locationDescriptor):
        self.locationDescriptor = locationDescriptor
        return self

    def getTag(self):
        return self.tag

    def getMessage(self):
        return self.message

    def getMessageRecipients(self):
        return self.messageRec

    def getLocationDescriptor(self):
        return self.locationDescriptor

    def __str__(self):
        return (
            "Tag: " + self.tag + "\n" +
            "Message: " + str(self.message) + "\n" +
            "Location Descriptor: " + str(self.locationDescriptor) + "\n" +
            "Message Recipients: " + str(self.messageRec)
        )

""" Test Functions """
def test_parseMessage():
    # message = (
    #     "danger there is a rebel army " +
    #     "coming this way near the awesome village"
    # )

    message = "message students hey everybody"
    print "Message:", message
    pm = parseMessage(message)
    print pm

if __name__ == "__main__":
    test_parseMessage()


