from import_export import resources, fields
from .models import Sample

class SampleResource(resources.ModelResource):

    class Meta:
        model = Sample



class FullSampleResource(resources.ModelResource):
    name = fields.Field()
    alt_name1 = fields.Field()
    project = fields.Field()
    species = fields.Field()
    family_id = fields.Field()
    relationship = fields.Field()
    karyotype = fields.Field()
    other_genetic_info = fields.Field()
    gender = fields.Field()
    year_of_birth = fields.Field()
    sample_name = fields.Field()
    tube_name = fields.Field()
    type = fields.Field()
    o_tissue = fields.Field()
    parent_id = fields.Field()
    box_pos = fields.Field()
    conc = fields.Field()
    vol = fields.Field()
    weight = fields.Field()
    cells = fields.Field()

    class Meta:
        model = Sample
        export_order = ('name', 'alt_name1', 'project', 'species', 'family_id', 'relationship',
                        'karyotype', 'other_genetic_info', 'gender', 'year_of_birth',
                        'sample_name', 'tube_name', 'type', 'o_tissue', 'parent_id', 'box_pos'
                                                                                     'conc', 'vol', 'weight', 'cells')