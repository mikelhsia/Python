'''
@Date    : 2017-11-01
@Author  : Michael Hsia
@Link    : 
@Version : 0.0.1
'''
# If you are using your django project applications in standalone scripts, in other words, 
# without using manage.py - you need to manually call django.setup() first - it would 
# configure the logging and, what is important - populate apps registry.

from __future__ import unicode_literals
import random
from blog.models import Author, Article, Tag

import django

print("Starting Rango population script...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advancedQuery.settings')
django.setup()
populate()


author_name_list = ['Tsu.yu.hsia', 'Michael Hsia', 'Mikelhsia', 'Michael', 'mikk']
article_title_list = ['Django 教程', 'Python 教程', 'HTML 教程']
 
 
def create_authors():
    for author_name in author_name_list:
        author, created = Author.objects.get_or_create(name=author_name)
        # 随机生成9位数的QQ，
        author.qq = ''.join(
            str(random.choice(range(10))) for _ in range(11)
        )
        author.addr = 'addr_%s' % (random.randrange(1, 3))
        author.email = '%s@hotmail.com' % (author.addr)
        author.save()
 
 
def create_articles_and_tags():
    # 随机生成文章
    for article_title in article_title_list:
        # 从文章标题中得到 tag
        tag_name = article_title.split(' ', 1)[0]
        tag, created = Tag.objects.get_or_create(name=tag_name)
 
        random_author = random.choice(Author.objects.all())
 
        for i in range(1, 21):
            title = '%s_%s' % (article_title, i)
            article, created = Article.objects.get_or_create(
                title=title, defaults={
                    'author': random_author,  # 随机分配作者
                    'content': '%s 正文' % title,
                    'score': random.randrange(70, 101),  # 随机给文章一个打分
                }
            )
            article.tags.add(tag)
 
 
def main():
    create_authors()
    create_articles_and_tags()
 
 
if __name__ == '__main__':
    main()
    print("Done!")