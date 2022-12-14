from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.

class PostCategory(models.Model):
    posts = models.ForeignKey('Post', on_delete=models.CASCADE)
    categories = models.ForeignKey('Category', on_delete=models.CASCADE)


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        c_rate = 0
        p_rate = 0
        post_rate = self.writer.aggregate(postRating=Sum('rating'))
        comment_rate = self.author.comment_set.aggregate(commentRating=Sum('rating'))
        c_rate += comment_rate.get('commentRating')
        p_rate += post_rate.get('postRating')

        self.author_rating = p_rate * 3 + c_rate
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=32, unique=True)


class Post(models.Model):
    posts = [
        ('news', 'Новость'),
        ('article', 'Статья')
    ]

    post_type = models.CharField(max_length=8, choices=posts, default='news')
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='writer')
    title = models.CharField(max_length=128)
    post_content = models.TextField()
    post_creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.post_content[:125]}..."


class Comment(models.Model):
    comment_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    comment_creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
