from sloth.userinput import ConversionFailed


def PresentConversionFailed(message):
    try:
        raise ConversionFailed(message)
    except ConversionFailed as e:
        print(e.failure_message)


def main(choose_, settings):
    message = 'This still needs worked on..'
    PresentConversionFailed(message)
