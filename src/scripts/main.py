import yaml
from slugify import slugify
from markdown import markdown as md
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from md2lds import Md2Lds

def slugify_url(item):
    item['slug'] = slugify(item['title'])
    return item

TODAY = datetime.today().date().isoformat()
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
    with open('posts/2020-06-20-a-demo.html', 'w') as rendered_post:
        render = post_page_template.render(
            sidebar=repositories,
            content={
                'text': md(post.read(), extensions=[Md2Lds()])
            },
            build_date=TODAY
        )
        rendered_post.write(render)
        rendered_post.close()
    post.close()

for project in content['projects']:
    with open('projects/{}.html'.format(project['slug']), 'w') as page:
        with open('content/source/projects/{}'.format(project['description'])) as project_md:
            project['description'] = md(project_md.read(), extensions=[Md2Lds()])
            project_md.close()

        project['sidebar'] = repositories
        project_page_render = project_page_template.render(
            detail=project,
            build_date=TODAY
        )
        page.write(project_page_render)
        page.close()

r = home_template.render(page={
    'sidebar': repositories,
    'build_date': TODAY
})

with open('index.html', 'w') as index_file:
    index_file.write(r)
