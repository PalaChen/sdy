from django import conf


def cxmadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('{}.cxmadmin'.format(app_name))
            # print('mod--->',mod)
        except ImportError:
            pass
