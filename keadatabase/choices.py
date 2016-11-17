CONTRIBUTOR_CHOICES = (
    ('', ''),
    ('TO', 'Tourist'),
    ('LO', 'Local'),
    ('SC', 'School group'),
    ('CG', 'Community group'),
    ('TR', 'Tramper'),
    ('HU', 'Hunter'),
    ('BI', 'Birder'),
    ('DO', 'DOC Staff'),
    ('OT', 'Other'),
)

ACCURACY_CHOICES = (
    ('', 'Unknown'),
    ('G', 'GPS coordinates'),
    ('E', 'Estimate from map'),
    ('O', 'Other'),
)

BAND_CHOICES = (
    ('', 'Couldn\'t tell'),
    ('U', 'Banded, unreadable'),
    ('B', 'Banded, readable'),
    ('N', 'Not banded'),
)

VERIFICATION_CHOICES = (
    ('', '(-) Unverified'),
    ('0', '(0) Bad'),
    ('1', '(1) OK'),
    ('2', '(2) Confirmed'),
)

SEX_CHOICES = (
    ('', 'Unknown'),
    ('F', 'Female'),
    ('M', 'Male'),
)

LIFE_STAGE_CHOICES = (
    ('', 'Unknown'),
    ('A', 'Adult'),
    ('S', 'Sub-adult'),
    ('J', 'Juvenile'),
    ('F', 'Fledgling'),
)

STATUS_CHOICES = (
    ('A', 'Alive'),
    ('D', 'Dead'),
)

LEG_CHOICES = (
    ('', 'Unknown'),
    ('L', 'Left'),
    ('R', 'Right'),
)

BAND_COLOUR_CHOICES = (
    ('BLACK', 'Black'),
    ('WHITE', 'White'),
    ('RED', 'Red'),
    ('ORANGE', 'Orange'),
    ('YELLOW', 'Yellow'),
    ('GREEN', 'Green'),
    ('BLUE', 'Blue'),
    ('GREY', 'Grey'),
    ('O', 'Other'),
)

BAND_SYMBOL_COLOUR_CHOICES = (
    ('WHITE', 'White'),
    ('BLACK', 'Black'),
    ('RED', 'Red'),
    ('YELLOW', 'Yellow'),
    ('O', 'Other'),
)

BAND_TYPE_CHOICES = (
    ('', 'Unknown'),
    ('P', 'Plastic (modern)'),
    ('M', 'Metal (historic)'),
)
