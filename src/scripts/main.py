import yaml
from slugify import slugify
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def slugify_url(item):
    item['slug'] = slugify(item['title'])
    return item

env = Environment(loader=FileSystemLoader(searchpath='src/templates'))

test_template = env.get_template('base.html')

content = yaml.load(open('content/projects.yaml').read(), Loader=yaml.SafeLoader)
# posts = yaml.load(open('content/posts.yaml').read(), Loader=yaml.SafeLoader)

content['projects'] = [slugify_url(x) for x in content['projects']]

project_page_template = env.get_template('project.html')
post_page_template = env.get_template('post.html')
repositories = env.get_template('repositorylist.html').render(items=content['projects'])

# for post in content['posts']:
#     with open('pages/posts/{}.html'.format(post['slug']), 'w') as page:
#         post['repositories'] = repositories
#         page.write(post_page_template.render(
#             detail=post
#         ))

today = datetime.today().date().isoformat()

for project in content['projects']:
    with open('pages/projects/{}.html'.format(project['slug']), 'w') as page:
        project['repositories'] = repositories
        project_page_render = project_page_template.render(
            detail=project,
            build_date=today
        )
        # print(project['description'].replace('\n', '</br>') if 'description' in project else '')
        page.write(project_page_render)
        page.close()

r = test_template.render(page={
    'content': 'Hello world',
    'repositories': repositories,
    'build_date': today
})

with open('index.html', 'w') as index_file:
    index_file.write(r)
