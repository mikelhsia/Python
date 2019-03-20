# Less Boilerplate with attr

import attr

# just pass frozen=True to attr.s() to make the class instances immutable.
@attr.s(frozen=True)
class Car(object):
    color = attr.ib()
    speed = attr.ib(default=0)

# Car("Blue")
# Out[3]: Car(color='Blue', speed=0)

    @speed.validator
    def speed_validator(self, attribute, value):
        if value < 0:
            raise ValueError('Value cannot be negative')


# Car("Blue",3).color = 'Red'
#   File "/usr/local/lib/python3.7/site-packages/attr/_make.py", line 429, in _frozen_setattrs
#     raise FrozenInstanceError()
# attr.exceptions.FrozenInstanceError
