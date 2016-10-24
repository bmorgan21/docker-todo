from todo_app import app  # noqa

if __name__ == '__main__':
    print '###'
    print '# Application Routes:'
    print '##'

    rules = [x for x in app.url_map.iter_rules()]
    rules.sort(lambda x, y: cmp(str(x.rule), str(y.rule)))
    for rule in rules:
        print '    {} ({}) -> {}'.format(rule, ', '.join(rule.methods), rule.endpoint)
