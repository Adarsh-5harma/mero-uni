import sys
sys.path.append("..")

from typing import get_args
from schemas import ResourceMetadata

def test_resource_type_allowed_vslues():
    expected_slugs = [
        'notes',
        'question-bank',
        'lab-solutions',
        'assignments',
        'past-papers',
        'syllabus'
    ]

    allowed_values = list(get_args(ResourceMetadata.model_fields['resource_type'].annotation))
    assert allowed_values == expected_slugs, f"Schema mismatch! Expected {expected_slugs}, but got {allowed_values}"