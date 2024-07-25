"""
Tests related migration to Pydantic 2.0
"""
import re
from json import loads
from typing import Optional, Literal
from unittest import TestCase

from pydantic import BaseModel, ValidationError, model_validator, parse_obj_as, TypeAdapter, validator, \
    field_validator, \
    Field, Extra

from wxc_sdk.person_settings.permissions_out import OutgoingPermissions


class TestOptional(TestCase):
    def test_001_optional_attribute_is_required(self):
        class TestModel(BaseModel):
            a: str
            b: Optional[str]

        data = {'a': 'a value'}
        with self.assertRaises(ValidationError) as exc:
            parsed = TestModel.model_validate(data)
        foo = 1

    def test_002_optional_attribute_can_be_none(self):
        class TestModel(BaseModel):
            a: str
            b: Optional[str]

        data = {'a': 'a value', 'b': None}
        parsed = TestModel.model_validate(data)

    def test_003_root_validator(self):
        class TestModel(BaseModel):
            a: str
            b: str

            @model_validator(mode='before')
            def val_root_test_model(cls, v):
                fa = re.findall(r'\s*([a-z]+)\s*=\s*(\w+),?', v)
                v = {k: v for k, v in fa}
                return v

        data = 'a=abc, b=def'
        parsed = TestModel.model_validate(data)
        foo = 1

    def test_004_root_validator_with_class(self):
        class Attribute(BaseModel):
            a: str
            b: int
            c: Literal['on', 'off']

        class Object(BaseModel):
            name: str
            a: Attribute

            @model_validator(mode='before')
            def val_root_object(cls, v):
                v['a'] = Attribute(a='a', b='10', c='on')
                return v

        parsed = Object(name='name')

    def test_005_parse_obj_as(self):
        class Test(BaseModel):
            number: int

        data = [{'number': i} for i in range(10)]
        parsed = parse_obj_as(list[Test], data)
        foo = 1

        parsed = TypeAdapter(list[Test]).validate_python(data)
        foo = 1

    def test_006_copy(self):
        class Test(BaseModel):
            a: str
            b: str

        obj = Test(a='a', b='b')
        c = obj.model_copy(deep=True)
        mc = obj.model_copy(deep=True)

    def test_007_validator(self):
        class Test(BaseModel):
            flag: bool
            new_flag: bool

            @staticmethod
            def do_validate(v):
                if v == 'on':
                    return True
                elif v == 'off':
                    return False
                else:
                    raise ValueError('"on" or "off" expected')

            @validator('flag', pre=True)
            def val_flg(cls, v):
                return cls.do_validate(v)

            @field_validator('new_flag', mode='before')
            def vaL_new_flag(cls, v):
                return cls.do_validate(v)

        o1 = Test.model_validate({'flag': 'on', 'new_flag': 'on'})
        foo = 1

    def test_008_bool_literal(self):
        class Test(BaseModel):
            flag: Literal[True] = Field(default=True)

        with self.assertRaises(ValidationError) as exc:
            t1 = Test.model_validate({'flag': False})

    def test_009_add_attribute_in_root_valdiator(self):
        class Att(BaseModel):
            a_1: int
            a_2: int

        class Test(BaseModel):
            a: Att
            b: Att

            class Config:
                extra = Extra.allow

            @model_validator(mode='before')
            def val_root_test(cls, v):
                v['c'] = Att(a_1=21, a_2=22)
                return v

        data = {'a': {'a_1': 1, 'a_2': 2},
                'b': {'a_1': 11, 'a_2': 12}}
        t = Test.model_validate(data)
        print(t)

    def test_010_outgoing_call_type_perms(self):
        json_txt = """{
    "useCustomEnabled": false,
    "callingPermissions": [
      {
        "callType": "INTERNAL_CALL",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "LOCAL",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "TOLL_FREE",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "TOLL",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "NATIONAL",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "INTERNATIONAL",
        "action": "BLOCK",
        "transferEnabled": false
      },
      {
        "callType": "OPERATOR_ASSISTED",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "CHARGEABLE_DIRECTORY_ASSISTED",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "SPECIAL_SERVICES_I",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "SPECIAL_SERVICES_II",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "PREMIUM_SERVICES_I",
        "action": "BLOCK",
        "transferEnabled": false
      },
      {
        "callType": "PREMIUM_SERVICES_II",
        "action": "BLOCK",
        "transferEnabled": false
      },
      {
        "callType": "CASUAL",
        "action": "BLOCK",
        "transferEnabled": false
      },
      {
        "callType": "URL_DIALING",
        "action": "ALLOW",
        "transferEnabled": true
      },
      {
        "callType": "UNKNOWN",
        "action": "ALLOW",
        "transferEnabled": true
      }
    ]
  }
"""
        data = loads(json_txt)
        op: OutgoingPermissions = OutgoingPermissions.model_validate(data)
        cp = op.calling_permissions
        cp_fields = cp.__dict__
        cp_dump = cp.model_dump()
        op_dump = op.model_dump()
        op_json = loads(op.model_dump_json())
        print(op)
        print(op.calling_permissions.casual)

    def test_010_can_include_override_exclude_none(self):
        class Test(BaseModel):
            a: Optional[str] = None

        data = {}
        t = Test.model_validate(data)
        print(t.model_dump_json())
        print(t.model_dump_json(exclude_none=True))
        print(t.model_dump_json(exclude_none=True, include={'a': True}))
        print(t.model_dump_json(exclude_unset=True))



