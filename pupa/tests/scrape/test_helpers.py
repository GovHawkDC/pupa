from pupa.scrape import Person, Organization
from pupa.utils import get_psuedo_id


def test_legislator_related_district():
    l = Person('John Adams', district='1', primary_org='legislature')
    l.pre_save('jurisdiction-id')

    assert len(l._related) == 1
    assert l._related[0].person_id == l._id
    assert get_psuedo_id(l._related[0].organization_id) == {'classification': 'legislature'}
    assert get_psuedo_id(l._related[0].post_id) == {"organization__classification": "legislature",
                                                    "label": "1"}
    assert l._related[0].role == 'member'


def test_legislator_related_chamber_district():
    l = Person('John Adams', district='1', primary_org='upper')
    l.pre_save('jurisdiction-id')

    assert len(l._related) == 1
    assert l._related[0].person_id == l._id
    assert get_psuedo_id(l._related[0].organization_id) == {'classification': 'upper'}
    assert get_psuedo_id(l._related[0].post_id) == {"organization__classification": "upper",
                                                    "label": "1"}
    assert l._related[0].role == 'member'


def test_legislator_related_party():
    l = Person('John Adams', district='1', party='Democratic-Republican')
    l.pre_save('jurisdiction-id')

    # a party membership
    assert len(l._related) == 2
    assert l._related[1].person_id == l._id
    assert get_psuedo_id(l._related[1].organization_id) == {'classification': 'party',
                                                            'name': 'Democratic-Republican'}
    assert l._related[1].role == 'member'


def test_committee_add_member_person():
    c = Organization('Defense', classification='committee')
    p = Person('John Adams')
    c.add_member(p, role='chairman')
    assert c._related[0].person_id == p._id
    assert c._related[0].organization_id == c._id
    assert c._related[0].role == 'chairman'


def test_committee_add_member_name():
    c = Organization('Defense', classification='committee')
    c.add_member('John Adams')
    assert get_psuedo_id(c._related[0].person_id) == {'name': 'John Adams'}
    assert c._related[0].organization_id == c._id
    assert c._related[0].role == 'member'
