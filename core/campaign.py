__author__ = 'pythoo'


class Campaigns:
    """
    Campaign Monitor is used to make Email campaign.
    """

    @staticmethod
    def campaign_factory(type):
        """
        This is the Factory method
        :return:
        """
        if type == 'MC':
            return MailChimp()
        if type == 'CM':
            return CakeMail()
        if type == 'DI':
            return DialogInsight()


class MailChimp(Campaigns):
    """
    Mail Chimp is one campaign monitor
    """

    @staticmethod
    def call_api():
        """
        Function to call the Mail Chimp api
        :return:
        """
        # TODO Make a api call to MailChimp
        print 'Call Mail Chimp API (see console)'


class CakeMail(Campaigns):
    """
    Cake Mail is one campaign monitors
    """

    @staticmethod
    def call_api():
        """
        Function to call the Cake Mail api
        :return:
        """
        # TODO Make a api call to Cake Mail
        print 'Call Cake Mail API (see console)'


class DialogInsight(Campaigns):
    """
    Dialog Insight is one campaign monitor
    """

    @staticmethod
    def call_api():
        """
        Function to call the Dialog Insight api
        :return:
        """
        # TODO Make a api call to Dialog Insight
        print 'Call Dialog Insight API (see console)'