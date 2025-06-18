from django.contrib import admin
from .models import (
    HomeModel,
    AboutUsHighlightModel,
    AboutUsModel,
    WeddingCategoryModel,
    GalleryModel,
    PriceHighLightModel,
    PriceModel,
    PriceTypeModel,
    BookModel,
    NewsModel,
    PositionModel,
    TeamMemberModel,
    WebContactInfoModel,
    WebSocialMedia,
    QrCodeModel,
    DashboardStatsModel,
)

admin.site.register(HomeModel)
admin.site.register(AboutUsHighlightModel)
admin.site.register(AboutUsModel)
admin.site.register(WeddingCategoryModel)
admin.site.register(GalleryModel)
admin.site.register(PriceHighLightModel)
admin.site.register(PriceModel)
admin.site.register(PriceTypeModel)
admin.site.register(BookModel)
admin.site.register(NewsModel)
admin.site.register(PositionModel)
admin.site.register(TeamMemberModel)
admin.site.register(WebContactInfoModel)
admin.site.register(WebSocialMedia)
admin.site.register(QrCodeModel)
admin.site.register(DashboardStatsModel)
