import os
from datetime import datetime
from operator import attrgetter
from dataclasses import dataclass

import yaml
from slugify import slugify
from markdown import markdown as md
from jinja2 import Environment, FileSystemLoader

from md2lds import Md2Lds
from mdmetadata import parse_markdown


def slugify_url(item):
    item['slug'] = slugify(item['title'])
    return item


TODAY = datetime.today().date().isoformat()
env = Environment(loader=FileSystemLoader(searchpath='src/templates'))

home_template = env.get_template('home.html')

content = yaml.load(open('content/projects.yaml').read(), Loader=yaml.SafeLoader)

content['projects'] = [slugify_url(x) for x in content['projects']]

project_page_template = env.get_template('project.html')
post_page_template = env.get_template('post.html')
repositories = env.get_template('repositorylist.html').render(items=content['projects'])
posts = []


for dire, fol, files in os.walk('content/source/posts'):
    for file in files:
        with open('{}/{}'.format(dire, file), 'r') as post:
            post_data = parse_markdown(post)
            fname = '{}-{}.html'.format(post_data.publish_date, file.replace('.md', ''))
            post_data.metadata['url'] = 'posts/{}'.format(fname)

            with open('{}/{}'.format('posts', fname), 'w') as rendered_post:
                print('Rendering post {} as {}...'.format(file, fname), end='')
                rendered_html = md(''.join(post_data.content), extensions=[Md2Lds()])
                render = post_page_template.render(
                    sidebar=repositories,
                    content=rendered_html,
                    build_date=TODAY,
                    metadata=post_data.metadata
                )
                rendered_post.write(render)
                rendered_post.close()
            post.close()
            posts.append(post_data)
            print(' OK')

posts.sort(key=attrgetter('publish_date'), reverse=True)

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


r = home_template.render(
    build_date=TODAY,
    page={
        'sidebar': repositories,
        'recent_posts': posts[:5]
    }
)

with open('index.html', 'w') as index_file:
    index_file.write(r)
