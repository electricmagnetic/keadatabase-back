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
    ('+', 'Alive'),
    ('-', 'Dead'),
)

BAND_STATUS_CHOICES = (
    ('+', 'Active'),
    ('-', 'Decommissioned'),
)

BAND_LEG_CHOICES = (
    ('', 'Unknown'),
    ('L', 'Left'),
    ('R', 'Right'),
)

BAND_POSITION_CHOICES = (
    ('', 'Unknown'),
    ('T', 'Top'),
    ('B', 'Bottom'),
    ('S', 'Single'),
)

BAND_STYLE_CHOICES = (
    ('', 'Unknown'),
    ('P', 'Plastic'),
    ('UM', 'Metal (uncoated)'),
    ('CM', 'Metal (powder coated)'),
)

BAND_COMBO_CHOICES = (
    ('L', 'Letter Combo (New)'),
    ('C', 'Colour Combo (Old)'),
)

BAND_SIZE_CHOICE = (
    ('', 'Unspecified'),
    ('SM', 'Small'),
    ('LG', 'Large'),
)

BAND_COLOUR_CHOICES = (
    ('', ''),
    ('BLACK', 'Black'),
    ('BLUE', 'Blue'),
    ('GREEN', 'Green'),
    ('LIME', 'Lime'),
    ('METAL', 'Metal'),
    ('ORANGE', 'Orange'),
    ('PINK', 'Pink'),
    ('PURPLE', 'Purple'),
    ('RED', 'Red'),
    ('WHITE', 'White'),
    ('YELLOW', 'Yellow'),
    ('O', 'Other'),
)

BAND_SYMBOL_COLOUR_CHOICES = (
    ('', ''),
    ('WHITE', 'White'),
    ('BLACK', 'Black'),
    ('RED', 'Red'),
    ('YELLOW', 'Yellow'),
    ('O', 'Other'),
)

BAND_SYMBOL_CHOICES = (
    ('', ''),
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    ('H', 'H'),
    ('I', 'I'),
    ('J', 'J'),
    ('K', 'K'),
    ('L', 'L'),
    ('M', 'M'),
    ('N', 'N'),
    ('O', 'O'),
    ('P', 'P'),
    ('Q', 'Q'),
    ('R', 'R'),
    ('S', 'S'),
    ('T', 'T'),
    ('U', 'U'),
    ('V', 'V'),
    ('W', 'W'),
    ('X', 'X'),
    ('Y', 'Y'),
    ('Z', 'Z'),
    ('!', '!'),
    ('"', '"'),
    ('#', '#'),
    ('$', '$'),
    ('%', '%'),
    ('&', '&'),
    ('\'', '\''),
    ('(', '('),
    (')', ')'),
    ('*', '*'),
    ('+', '+'),
    (',', ','),
    ('-', '-'),
    ('.', '.'),
    ('/', '/'),
    (':', ':'),
    (';', ';'),
    ('<', '<'),
    ('=', '='),
    ('>', '>'),
    ('?', '?'),
    ('@', '@'),
    ('[', '['),
    ('\\', '\\'),
    (']', ']'),
    ('^', '^'),
    ('_', '_'),
    ('`', '`'),
    ('{', '{'),
    ('|', '|'),
    ('}', '}'),
    ('~', '~'),
    ('obelus', 'Divide'),
    ('theta', 'Theta'),
)
