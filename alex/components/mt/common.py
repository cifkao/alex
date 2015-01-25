from __future__ import unicode_literals

from alex.components.mt.exceptions import MTException


def get_mt_type(cfg):
    """
    Reads the MT type from the configuration.
    """
    return cfg['MT']['type']


def mt_factory(cfg, mt_type=None):
    ''' Returns an instance of the MT module
    specified in mt_type.
    '''
    if mt_type is None:
        mt_type = get_mt_type(cfg)
    t = get_mt_type(cfg)

    if t == 'MTMonkey':
        from alex.components.mt.mtmonkey import MTMonkeyMT
        mt = MTMonkeyMT(cfg)
    else:
        raise MTException('Unsupported MT module: %s' % mt_type)

    return mt
