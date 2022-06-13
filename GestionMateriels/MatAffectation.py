from database import Base
from sqlalchemy import Column, ForeignKey, Table


mat_affectation_bureau = Table("mat_affectation_bureau",
                               Base.metadata,
                               Column("num_aff", ForeignKey("affectations.numa"), primary_key=True),
                               Column("code_inv_bureau", ForeignKey("bureautiques.code_inv"), primary_key=True),
                               )

mat_affectation_info = Table("mat_affectation_info",
                             Base.metadata,
                             Column("num_aff", ForeignKey("affectations.numa"), primary_key=True),
                             Column("code_inv_info", ForeignKey("informatiques.code_inv"), primary_key=True))
