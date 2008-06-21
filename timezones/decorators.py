from django.utils.encoding import smart_str

import pytz

utc_tz = pytz.timezone('UTC')

def localdatetime(fieldname):
    def get_datetime(inst):
        return getattr(inst, fieldname)
    def set_datetime(inst, val):
        return setattr(inst, fieldname, val)

    def make_local_property(get_tz):
        def getlocal(inst):
            tz = get_tz(inst)
            if not hasattr(tz, 'localize'):
                tz = pytz.timezone(smart_str(tz))
            dt = get_datetime(inst)
            if dt.tzinfo is None:
                dt = utc_tz.localize(dt)
            return dt.astimezone(tz)
        def setlocal(inst, dt):
            if dt.tzinfo is None:
                tz = get_tz(inst)
                if not hasattr(tz, 'localize'):
                    tz = pytz.timezone(smart_str(tz))
                dt = tz.localize(dt)
            dt = dt.astimezone(utc_tz)
            return set_datetime(inst, dt)
        return property(getlocal, setlocal)
    return make_local_property
