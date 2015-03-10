
from passlib.hash import md5_crypt


class CiscoPassword(object):
    def __init__(self):
        md5_crypt.max_salt_size = 3  # cisco uses a salt length of 3
        md5_crypt.min_salt_size = 3

    def secret5(self, clear_secret):
        """ take clear_secret and return a cisco level5 hash
        """

        return md5_crypt.encrypt(clear_secret)

    def decrypt7(self, clear_7):
        """ decrypt cisco level 7 password
        """

        decrypt = lambda x: ''.join([chr(int(x[i:i+2], 16)^ord('dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'[(int(x[:2])+i/2-1) % 53])) for i in range(2, len(x), 2)])
        return decrypt(clear_7)

    def gen_ios(self, clear_secret, level=None):
        """ generate a cisco IOS enable secret string

            cisco_pw = CiscoPassword()
            cisco_pw.gen_ios('letmein')
            enable secret 5 $1$56p$gaPedzD8P9o7euEP9fsaI/
        """

        secret = self.secret5(clear_secret)
        if level:
            return 'enable secret level {level} 5 {secret}'.format(level=level, secret=secret)
        else:
            return 'enable secret 5 {secret}'.format(secret=secret)

    def gen_catos(self, clear_secret):
        """ generate a cisco CATos enable secret string

            cisco_pw = CiscoPassword()
            cisco_pw.gen_catos('letmein')
            enable secret 5 $2$56p$gaPedzD8P9o7euEP9fsaI/
        """

        secret = '$2' + self.secret5(clear_secret)[2:]
        return 'set password {}\nset enablepass {}'.format(secret, secret)

    def gen_nxos(self, clear_secret, user='admin'):
        """ generate a cisco NXOS admin password string
        """

        secret = self.secret5(clear_secret)
        return 'username {user} password 5 {secret}  role network-admin'.format(user=user, secret=secret)

    def gen_ace(self, clear_secret, user):
        """ generate a cisco ACE admin password string
        """

        secret = self.secret5(clear_secret)
        return 'username {user} password 5 {secret}  role Admin domain default-domain'.format(user=user, secret=secret)
