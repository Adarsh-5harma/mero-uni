import sys
sys.path.append("..") 

import pytest
from pydantic import ValidationError
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


    import pytest
from pydantic import ValidationError

# (Your existing test_resource_type_allowed_values is up here)
# ... 

def test_semester_out_of_bounds():
    """Test that a semester > 8 is rejected by Pydantic."""
    with pytest.raises(ValidationError):
        ResourceMetadata(
            resource_type="notes",
            semester=9,  # 9 is invalid (ge=1, le=8)
            subject="Math",
            key_topics=["Algebra"],
            summary="Test."
        )

def test_unknown_resource_type():
    """Test that a made-up resource type is rejected."""
    with pytest.raises(ValidationError):
        ResourceMetadata(
            resource_type="hacking-notes",  # Not in the Literal list
            semester=5,
            subject="Security",
            key_topics=["Bypassing firewalls"],
            summary="Test."
        )

def test_extra_fields_are_forbidden():
    """Test that the AI cannot sneak in extra fields (extra='forbid')."""
    with pytest.raises(ValidationError):
        ResourceMetadata(
            resource_type="notes",
            semester=5,
            subject="Math",
            key_topics=["Algebra"],
            summary="Test.",
            difficulty="hard"  # Extra field!
        )

def test_semester_can_be_null():
    """Test that a missing semester is allowed and doesn't cause a crash."""
    metadata = ResourceMetadata(
        resource_type="notes",
        semester=None,  # <-- This should now be allowed
        subject="Math",
        key_topics=["Algebra"],
        summary="Test."
    )
    assert metadata.semester is None