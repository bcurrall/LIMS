# tutorial/tables.py
from django_tables2 import A
import django_tables2 as tables
from django import forms
from .models import Individual, Sample, Freezer, FreezerPos, Box
import project

class IndividualTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Individual
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class SampleTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}



class FullSampleTable(tables.Table):
    id = tables.Column(accessor='pk')
    name = tables.Column(accessor='individual.name')
    alt_name1 = tables.Column(accessor='individual.alt_name1')
    alt_name2 = tables.Column(accessor='individual.alt_name2')
    project = tables.Column(accessor='individual.project')
    species = tables.Column(accessor='individual.species')
    family_id = tables.Column(accessor='individual.family_id')
    relationship = tables.Column(accessor='individual.relationship')
    karyotype = tables.Column(accessor='individual.karyotype')
    other_genetic_info = tables.Column(accessor='individual.other_genetic_info')
    gender = tables.Column(accessor='individual.gender')
    year_of_birth = tables.Column(accessor='individual.year_of_birth')
    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        exclude = {'individual', 'active'}
        sequence = ('id','name', 'alt_name1', 'alt_name2', 'project', 'species',
                    'family_id', 'relationship', 'karyotype', 'other_genetic_info', 'gender', 'year_of_birth',
                    'sample_name', 'tube_name', 'type', 'o_tissue', 'parent_id', 'box_pos', 'conc', 'vol', 'weight', 'cells')


class FreezerTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Freezer
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class BoxTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Box
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}