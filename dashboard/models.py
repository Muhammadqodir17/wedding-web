from django.db import models
from django.db.models import FloatField
from django.utils.translation import gettext_lazy as _

from core.base import BaseModel

SALARY_TYPE = (
    (1, 'Monthly'),
    (2, 'Daily'),
)


class HomeModel(BaseModel):
    title = models.CharField(_('title'), max_length=300)
    description = models.TextField(_('description'), )
    image = models.ImageField(_('image'), upload_to='media/', null=True)

    def __str__(self):
        return f'{self.title}'


class AboutUsHighlightModel(BaseModel):
    title = models.CharField(_('title'), max_length=300)
    description = models.TextField(_('description'), )

    def __str__(self):
        return f"{self.title}"

# 5
class AboutUsModel(BaseModel):
    title = models.CharField(_('title'), max_length=300)
    description = models.TextField(_('description'), )
    image = models.ImageField(_('image'), upload_to='media/', null=True)
    highlight = models.ManyToManyField(AboutUsHighlightModel)
    main_description = models.TextField(_('main_description'), )
    successful_events = models.IntegerField(_('successful_events'), default=0)
    work_experience = models.IntegerField(_('work_experience'), default=0)

    def __str__(self):
        return f'{self.title}'

# 3
class WeddingCategoryModel(BaseModel):
    name = models.CharField(_('name'), max_length=250)
    description = models.TextField(_('description'), )
    image = models.ImageField(_('image'), upload_to='media/', null=True)

    def __str__(self):
        return f"{self.name}"


class GalleryModel(BaseModel):
    category = models.ForeignKey(WeddingCategoryModel, on_delete=models.CASCADE)
    image = models.ImageField(_('image'), upload_to='media/', null=True)

    def __str__(self):
        return f"{self.category}"




class PriceTypeModel(BaseModel):
    name = models.CharField(_('name'), max_length=250)

    def __str__(self):
        return f'{self.name}'


# 4
class PriceModel(BaseModel):
    type = models.CharField(max_length=250)
    price = FloatField(_('price'), default=0)
    description = models.TextField(_('description'), )

    def __str__(self):
        return f'{self.type}'


class PriceHighLightModel(BaseModel):
    price = models.ForeignKey(PriceModel, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(_('description'), )

    def __str__(self):
        return f'{self.description}'

# 2
class BookModel(BaseModel):
    category = models.ForeignKey(WeddingCategoryModel, on_delete=models.CASCADE)
    book_date = models.DateField(_('book_date'), )
    booker_first_name = models.CharField(_('booker_first_name'), max_length=250)
    booker_last_name = models.CharField(_('booker_last_name'), max_length=250)
    phone_number = models.CharField(_('phone_number'), max_length=13)
    number_of_guests = models.PositiveIntegerField(_('number_of_guests'), default=0)
    price = models.FloatField(_('price'), default=0)
    additional_info = models.TextField(_('additional_info'), )

    def __str__(self):
        return f"{self.book_date}"


class NewsModel(BaseModel):
    title = models.CharField(_('title'), max_length=300)
    description = models.TextField(_('description'), )
    image = models.ImageField(_('image'), upload_to='media/', null=True)

    def __str__(self):
        return f"{self.title}"


class PositionModel(BaseModel):
    name = models.CharField(_('name'), max_length=250)

    def __str__(self):
        return f"{self.name}"

# 1
class TeamMemberModel(BaseModel):
    first_name = models.CharField(_('first_name'), max_length=250)
    last_name = models.CharField(_('last_name'), max_length=250)
    middle_name = models.CharField(_('middle_name'), max_length=250)
    position = models.ForeignKey(PositionModel, on_delete=models.CASCADE)
    from_working_hours = models.TimeField(_('from_working_hours'), )
    to_working_hours = models.TimeField(_('to_working_hours'), )
    salary_type = models.IntegerField(_('salary_type'), choices=SALARY_TYPE, default=1)
    salary = models.FloatField(_('salary'), default=0)
    work_start_data = models.DateField(_('work_start_data'), )
    image = models.ImageField(_('image'), upload_to='media/', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 8
class WebContactInfoModel(BaseModel):
    wedding_hall_name = models.CharField(_('wedding_hall_name'), max_length=300)
    phone_number = models.CharField(_('phone_number'), max_length=13)
    email = models.EmailField(_('email'), )
    open_from = models.TimeField(_('open_from'), )
    close_to = models.TimeField(_('close_to'), )
    location = models.CharField(_('location'), max_length=300)
    location_url = models.CharField(_('location_url'), max_length=300, default='example.com')

    def __str__(self):
        return f"{self.email}"

# 7
class WebSocialMedia(BaseModel):
    name = models.CharField(_('name'), max_length=250)
    url = models.URLField(_('url'), )
    social_media_image = models.ImageField(_('social_media_image'), upload_to='media/', null=True)

    def __str__(self):
        return f"{self.id}"


class DashboardStatsModel(BaseModel):
    employees = models.IntegerField(_('employees'), default=0)
    events = models.IntegerField(_('events'), default=0)
    annual_income = models.IntegerField(_('annual_income'), default=0)
    unanswered_messages = models.IntegerField(_('unanswered_messages'), default=0)

    def __str__(self):
        return f'{self.employees}'


class QrCodeModel(BaseModel):
    url = models.URLField(_('url'), )
    image = models.ImageField(_('image'), upload_to='media/', blank=True, null=True)
