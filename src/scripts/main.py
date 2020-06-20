import yaml
from slugify import slugify
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def slugify_url(item):
    item['slug'] = slugify(item['title'])
    return item

env = Environment(loader=FileSystemLoader(searchpath='src/templates'))

home_template = env.get_template('home.html')

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

with open('content/source/posts/2020-06-20-a-demo.md', 'r') as post:
    with open('content/posts/2020-06-20-a-demo.html', 'w') as rendered_post:
        render = post_page_template.render(
            content={
                'text': markdown(post.read())
            }
        )
        rendered_post.write(render)
        rendered_post.close()
    post.close()

today = datetime.today().date().isoformat()

for project in content['projects']:
    with open('pages/projects/{}.html'.format(project['slug']), 'w') as page:
        project['sidebar'] = repositories
        project_page_render = project_page_template.render(
            detail=project,
            build_date=today
        )
        page.write(project_page_render)
        page.close()

r = home_template.render(page={
    'sidebar': repositories,
    'build_date': today
})

with open('index.html', 'w') as index_file:
    index_file.write(r)
