from django import template

from menu.app_data_types import Item, MenuTree
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('tags/menu.html', takes_context=True)
def show_menu(context, menu_title: str) -> dict:
    def _set_relationships(item: Item, items: list[Item]):
        if item.parent_id:
            parent = [i for i in items if i.id == item.parent_id][0]
            parent.children += [item]
            item.parent = parent
            pass

    def _tree_generator(items: list[Item],
                        depth: int = 0,
                        tree: MenuTree = None):
        for i in items:
            if i.parent is None or i.parent.active:
                tree.html += (f'<li>{"-" * depth} '
                              f'<a href="/{i.url}">{i.title}</a></li>')
            if i.children:
                _tree_generator(items=i.children,
                                depth=depth + 1,
                                tree=tree)

    def _get_active_item(url_type: str, items: list[Item]) -> Item | None:
        active_item = list(
            filter(lambda item: url_type in (item.url, item.named_url),
                   items)
        )
        if active_item:
            return active_item[0]

    def _set_item_tree_status(item: Item,
                              status: bool,
                              items: list[Item]) -> None:
        item.active = status
        if item.parent_id:
            parent = list(
                filter(lambda i: i.id == item.parent_id, items))[0]
            _set_item_tree_status(parent, status, items)

    url_type = context.request.resolver_match.kwargs.get('url_type')

    qs = MenuItem.objects.filter(
        menu__title=menu_title
    ).select_related('parent')
    menu_values = qs.values()

    menu_items = [Item(
        title=i['title'],
        id=i['id'],
        parent_id=i['parent_id'],
        url=i['url'],
        named_url=i['named_url'],
    ) for i in menu_values]

    # Получение списка тир-0 родителей
    parents = [i for i in menu_items if i.parent_id is None]

    # Установка родителей и наследников
    [_set_relationships(i, menu_items) for i in menu_items]

    # Установка активного пункта меню
    if url_type:
        active_item = _get_active_item(url_type=url_type,
                                       items=menu_items)
        if active_item:
            _set_item_tree_status(item=active_item,
                                  status=True,
                                  items=menu_items)

    # HTML обёртка. Пример
    html_tree = MenuTree('')
    html_tree.html += '<ul>'
    _tree_generator(items=parents, depth=0, tree=html_tree)
    html_tree.html += '</ul>'

    return {'menu': html_tree.html}
