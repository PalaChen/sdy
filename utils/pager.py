from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustonPaginator(Paginator):
    def __init__(self, current_page, per_page_num, *args, **kwargs):
        super(CustonPaginator, self).__init__(*args, **kwargs)
        try:
            # 当前页
            self.current_page = int(current_page)
        except:
            self.current_page = 1
        # 最多显示页码数量
        self.per_page_num = int(per_page_num)

    def pager_num_range(self):
        # 当前页
        # self.current_page
        # 最多显示的页码数量
        # self.per_page_num
        # 总页数
        # self.num_pages

        # 如果总页数小于显示页码数量
        if self.num_pages < self.per_page_num:
            return range(1, self.num_pages + 1)

        part = int(self.per_page_num / 2)
        # 如果总页数大于显示页码数量
        if self.current_page <= part:
            return range(1, self.per_page_num + 1)

        if (self.current_page + part) > self.num_pages:
            return range(self.num_pages - self.per_page_num, self.num_pages + 1)
        return range(self.current_page - part, self.current_page + part + 1)


def paginator(req, obj):
    current_page = req.GET.get('p')
    paginator = CustonPaginator(current_page, 9, obj, 10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts
