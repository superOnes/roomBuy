from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class Pagination:

    def __init__(self, queryset, page, num_page):
        self.queryset = queryset
        self.page = page
        self.num_page = num_page

    def get_queryset(self):
        self.paginator = Paginator(self.queryset, self.num_page)
        try:
            self.queryset = self.paginator.page(self.page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            self.queryset = self.paginator.page(1)  # 取第一页的记录
            self.page = 1
        except EmptyPage:  # 如果页码太大，没有相应的记录
            self.queryset = self.paginator.page(self.paginator.num_pages)
            self.page = self.paginator.num_pages
        return self.queryset

    def page_obj(self):
        page_obj = {
            'num_pages': self.paginator.num_pages,
            'number': self.page
        }
        return page_obj
