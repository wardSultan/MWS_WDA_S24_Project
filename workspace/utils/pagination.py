def paginate(queryset, page, pageSize):
    start = (page - 1) * pageSize
    end = start + pageSize
    return queryset[start:end]
