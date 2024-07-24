from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

User = get_user_model()

def user_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.title, filename)

class Postt(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='media', blank=True, null=True)

    #Devuelve el título del post como representación en cadena del objeto.
    def __str__(self):
        return self.title
    #Define la ordenación predeterminada en orden descendente.
    class Meta:
        ordering = ["-created_at", "-updated_at"]
    # Devuelve la URL de la API para obtener los detalles del post.
    def get_api_url(self):
        try:
            return reverse("posts_api:post_detail", kwargs={"slug": self.slug})
        except:
            None
    #Devuelve los comentarios asociados al post
    @property
    def comments(self):
        instance = self
        qs = Commen.objects.filter(parent=instance)
        return qs

#Genera un slug unico para el post
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Postt.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

#Si el slug no esta definicido, esta función genera un slug unico
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Postt)


class Commen(models.Model):
    parent = models.ForeignKey(Postt, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]