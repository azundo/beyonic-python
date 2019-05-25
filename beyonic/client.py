from beyonic.api_client import ApiClient
from beyonic.resources import GenericObject
from beyonic.errors import BeyonicError


class AbstractAPI(GenericObject):
    """
    AbtractApi class, all the other api class extends it
    """

    def __init__(self, api_key, api_endpoint_base, api_version, verify_ssl_certs):
        self.api_key = api_key
        self.verify_ssl_certs = verify_ssl_certs
        self.api_endpoint_base = api_endpoint_base
        self.api_version = api_version

    def get_client(self, client=None):
        url = self.get_url()
        # from beyonic import api_key, verify_ssl_certs, api_version
        if not client:
            client = None
        return ApiClient(api_key=self.api_key, url=url, client=client,
                         verify_ssl_certs=self.verify_ssl_certs, api_version=self.api_version)

    def get_url(self):
        api_endpoint_base = self.api_endpoint_base
        if not api_endpoint_base.endswith("/"):
            api_endpoint_base = api_endpoint_base + "/"
        cls_name = api_endpoint_base + str(self._method_path)
        return cls_name

    def list(self, client=None, **kwargs):
        """
        This will return list of resources.
        """
        objs = self.get_client(client).get(**kwargs)

        # setting client object for each of the return object so that it can be used while saving data
        for obj in objs.results:
            if obj.id:
                base = self.get_url()
                url = "%s/%s" % (base, obj.id)
                api_client = self.get_client(client)
                api_client.set_url(url)
                obj.set_client(api_client)

        return objs

    def create(self, client=None, **kwargs):
        """
        This will create new object
        """
        return self.get_client(client).post(**kwargs)

    def get(self, id, client=None, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')

        base = self.get_url()
        url = "%s/%s" % (base, id)
        api_client = self.get_client(client)
        api_client.set_url(url)
        obj = api_client.get(**kwargs)
        obj.set_client(api_client)
        return obj

    def update(self, id, client=None, **kwargs):
        """
        This will update the object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')
        base = self.get_url()
        url = "%s/%s" % (base, id)
        api_client = self.get_client(client)
        api_client.set_url(url)
        return api_client.patch(**kwargs)

    def delete(self, id, client=None, **kwargs):
        """
        This will return the single object
        """
        if not id:
            raise BeyonicError('Invalid ID or ID hasn\'t been specified')

        base = self.get_url()
        url = "%s/%s" % (base, id)
        api_client = self.get_client(client)
        api_client.set_url(url)
        return api_client.delete(**kwargs)


class Payment(AbstractAPI):
    _method_path = 'payments'


class Webhook(AbstractAPI):
    _method_path = 'webhooks'


class Collection(AbstractAPI):
    _method_path = "collections"


class CollectionRequest(AbstractAPI):
    _method_path = "collectionrequests"


class Transaction(AbstractAPI):
    _method_path = "transactions"


class Account(AbstractAPI):
    _method_path = "accounts"


class Contact(AbstractAPI):
    _method_path = "contacts"


class Client(object):

    def __init__(self, api_key, api_endpoint_base, api_version=None, verify_ssl_certs=True):
        self.api_key = api_key
        self.api_endpoint_base = api_endpoint_base
        self.api_version = api_version
        self.verify_ssl_certs = verify_ssl_certs
        self.Payment = Payment(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.Webhook = Webhook(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.Collection = Collection(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.CollectionRequest = CollectionRequest(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.Transaction = Transaction(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.Account = Account(api_key, api_endpoint_base, api_version, verify_ssl_certs)
        self.Contact = Contact(api_key, api_endpoint_base, api_version, verify_ssl_certs)
