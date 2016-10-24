from helpers.script import Script
import sys
import smtplib
import socket
from helpers.result import Result
from tribool import Tribool
from email.mime.text import MIMEText


class Nmass_smtp(Script):


    def assess_finding(self):
        if self.finding['port'] == 25:
            return True
        return False


    def enumerate(self,finding):
        super(Nmass_smtp,self).enumerate(finding)
        return False


    def send(self,msg,address,sender,receiver):
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        try:
            s = smtplib.SMTP(address)
            s.sendmail(sender, receiver, msg.as_string())
            s.quit()
            return Tribool(None)
        except smtplib.SMTPRecipientsRefused: 
            return False
            pass
        except smtplib.SMTPServerDisconnected:
            return False
            pass
        except socket.error:
            return False
            pass


class Spoof(Nmass_smtp):
    def enumerate(self,finding):
        check = super(Nmass_smtp, self).enumerate(finding)
        if check is False:
            return False
        domains = self.config['spoof'].keys()
        configuration = self.config['spoof']
        for domain in domains:
            sender = configuration[domain]['from']
            receiver = configuration[domain]['from']
            msg = MIMEText(configuration[domain]['message'])
            msg['Subject'] = configuration[domain]['subject'] % (finding['address'])
            msg['From'] = sender
            msg['To'] = receiver
            send_result = super(Spoof, self).send(msg, finding['address'], sender, receiver)
            r = Result()
            if send_result is not False:
                r.module = sys.modules[__name__]
                r.classname = self.__class__.__name__
                r.finding = finding
                r.description = "Possible success of email sent from %s to %s" % (sender, receiver)
            return r


class Relay(Nmass_smtp):


    def enumerate(self,finding):
        check = super(Nmass_smtp, self).enumerate(finding)
        if check is False:
            return False
        domains = self.config['relay'].keys()
        configuration = self.config['relay']
        for domain in domains:
            sender = configuration[domain]['from']
            receiver = configuration[domain]['from']
            msg = MIMEText(configuration[domain]['message'])
            msg['Subject'] = configuration[domain]['subject'] % (finding['address'])
            msg['From'] = sender
            msg['To'] = receiver
            send_result = super(Relay, self).send(msg, finding['address'], sender, receiver)
            r = Result()
            if send_result is not False:
                r.module = sys.modules[__name__]
                r.classname = self.__class__.__name__
                r.finding = finding
                r.description = "Possible success of email sent from %s to %s" % (sender, receiver)
            return r
