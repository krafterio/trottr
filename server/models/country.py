from models.base import BaseModel
import edgy


class Country(BaseModel):
    name = edgy.CharField(max_length=100)
    iso_code = edgy.CharField(max_length=3, unique=True)

    class Meta:
        tablename = "countries"
