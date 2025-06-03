from django.db import models
from django.db.models import FloatField

from core.base import BaseModel

SALARY_TYPE = (
    (1, 'Monthly'),
    (2, 'Daily'),
)


class HomeModel(BaseModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f'{self.title}'


class AboutUsHighlightModel(BaseModel):
    title = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

# 5
class AboutUsModel(BaseModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True)
    highlight = models.ManyToManyField(AboutUsHighlightModel)
    main_description = models.TextField()
    successful_events = models.ImageField(default=0)
    work_experience = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'

# 3
class WeddingCategoryModel(BaseModel):
    name = models.CharField(max_length=250)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f"{self.name}"


class GalleryModel(BaseModel):
    category = models.ForeignKey(WeddingCategoryModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f"{self.category}"


class PriceHighLightModel(BaseModel):
    description = models.TextField()

    def __str__(self):
        return f'{self.description}'


class PriceTypeModel(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'


# 4
class PriceModel(BaseModel):
    type = models.ForeignKey(PriceTypeModel, on_delete=models.CASCADE, blank=True, null=True)
    price = FloatField(default=0)
    description = models.TextField()
    highlights = models.ManyToManyField(PriceHighLightModel)

    def __str__(self):
        return f'{self.type.name}'

# 2
class BookModel(BaseModel):
    category = models.ForeignKey(WeddingCategoryModel, on_delete=models.CASCADE)
    book_date = models.DateField()
    booker_first_name = models.CharField(max_length=250)
    booker_last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13)
    number_of_guests = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    additional_info = models.TextField()

    def __str__(self):
        return f"{self.book_date}"


class NewsModel(BaseModel):
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f"{self.title}"


class PositionModel(BaseModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"

# 1
class TeamMemberModel(BaseModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250)
    position = models.ForeignKey(PositionModel, on_delete=models.CASCADE)
    from_working_hours = models.TimeField()
    to_working_hours = models.TimeField()
    salary_type = models.IntegerField(choices=SALARY_TYPE, default=1)
    salary = models.FloatField(default=0)
    work_start_data = models.DateField()
    image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 8
class WebContactInfoModel(BaseModel):
    wedding_hall_name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField()
    open_from = models.TimeField()
    close_to = models.TimeField()
    location = models.CharField(max_length=300)
    location_url = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.email}"

# 7
class WebSocialMedia(BaseModel):
    name = models.CharField(max_length=250)
    url = models.URLField()
    social_media_image = models.ImageField(upload_to='media/', null=True)
    # facebook = models.URLField()
    # facebook_image = models.ImageField(upload_to='media/', null=True)
    # telegram = models.URLField()
    # telegram_image = models.ImageField(upload_to='media/', null=True)

    def __str__(self):
        return f"{self.id}"


class DashboardStatsModel(BaseModel):
    employees = models.IntegerField(default=0)
    events = models.IntegerField(default=0)
    annual_income = models.IntegerField(default=0)
    unanswered_messages = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.employees}'
