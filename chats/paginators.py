from rest_framework.pagination import PageNumberPagination


class ChatsPaginator(PageNumberPagination):
    """
    Пагинатор для приложения chats
    К-во элементов 5 (максимум 10) на странице
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10
